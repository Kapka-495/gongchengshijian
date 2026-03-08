/**
 * 材料 XRD 可视化 - 前端应用
 * 支持双数据集对比和相似度分析
 */

// 同源时使用相对路径，否则使用完整后端地址
const API_BASE = window.location.origin;

// 示例 XRD 峰数据 (角度, 强度)
const SAMPLE_DATA_1 = `25.5 100
26.2 85
38.1 120
44.2 95
51.8 110
64.2 78
77.4 65`;

const SAMPLE_DATA_2 = `25.8 95
26.5 90
38.4 115
44.5 90
52.1 105
64.5 75
77.7 60`;

// DOM 元素 - 数据集 1
const dataInput1 = document.getElementById("dataInput1");
const processBtn = document.getElementById("processBtn");
const loadSampleBtn1 = document.getElementById("loadSample1");
const npyFileInput1 = document.getElementById("npyFile1");
const npyFileLabel1 = document.getElementById("npyFileLabel1");
const npyFileInfo1 = document.getElementById("npyFileInfo1");
const npyFileDetails1 = document.getElementById("npyFileDetails1");
const groupIndexInput1 = document.getElementById("groupIndex1");
const refreshGroupBtn1 = document.getElementById("refreshGroupBtn1");

// DOM 元素 - 数据集 2
const dataInput2 = document.getElementById("dataInput2");
const loadSampleBtn2 = document.getElementById("loadSample2");
const npyFileInput2 = document.getElementById("npyFile2");
const npyFileLabel2 = document.getElementById("npyFileLabel2");
const npyFileInfo2 = document.getElementById("npyFileInfo2");
const npyFileDetails2 = document.getElementById("npyFileDetails2");
const groupIndexInput2 = document.getElementById("groupIndex2");
const refreshGroupBtn2 = document.getElementById("refreshGroupBtn2");

// 共享参数
const chartYModeSelect = document.getElementById("chartYMode");
const minAngleInput = document.getElementById("minAngle");
const maxAngleInput = document.getElementById("maxAngle");
const stepInput = document.getElementById("step");
const sigmaInput = document.getElementById("sigma");

// 图表和数据处理
let xrdChart1 = null;
let xrdChart2 = null;
let lastChartResult1 = null;
let lastChartResult2 = null;
let uploadedNpyFile1 = null;
let uploadedNpyFile2 = null;

// 当前选中的输入方式
function getActiveInputTab(datasetNum) {
  // 使用更可靠的选择器
  const datasetSections = document.querySelectorAll('.dataset-section');
  
  if (datasetSections.length < datasetNum) {
    console.log(`找不到数据集 ${datasetNum} 的 section，总共有 ${datasetSections.length} 个 section`);
    return `paste${datasetNum}`;
  }
  
  const section = datasetSections[datasetNum - 1]; // 转换为 0-based 索引
  const activeTab = section.querySelector('.method-tabs .tab.active');
  const tabName = activeTab ? activeTab.dataset.tab : `paste${datasetNum}`;
  console.log(`数据集 ${datasetNum} 当前激活标签:`, tabName);
  return tabName;
}

// 解析用户输入的 XRD 数据
function parseXRDInput(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  const data = [];

  for (const line of lines) {
    const parts = line.trim().split(/[\s\t,;]+/);
    if (parts.length >= 2) {
      const angle = parseFloat(parts[0]);
      const intensity = parseFloat(parts[1]);
      if (!isNaN(angle) && !isNaN(intensity)) {
        data.push({ angle, intensity });
      }
    }
  }

  return data;
}

// 计算数组的四分位数（Q1, Q2, Q3）及最大、最小值，包含对应的横坐标
function computeStatsWithAngles(angles, intensities) {
  if (!angles || !intensities || angles.length === 0 || intensities.length === 0) {
    return {
      min: { value: null, angle: null },
      max: { value: null, angle: null },
      q1: { value: null, angle: null },
      q2: { value: null, angle: null },
      q3: { value: null, angle: null }
    };
  }

  // 创建角度-强度对并排序
  const pairs = angles.map((angle, i) => ({ angle, intensity: intensities[i] }));
  const sortedByIntensity = [...pairs].sort((a, b) => a.intensity - b.intensity);
  const n = sortedByIntensity.length;

  // 找到最大值和最小值及其对应的角度
  const minPair = sortedByIntensity[0];
  const maxPair = sortedByIntensity[n - 1];

  // 计算四分位数对应的强度值
  const percentile = (p) => {
    const idx = p * (n - 1);
    const lo = Math.floor(idx);
    const hi = Math.ceil(idx);
    if (lo === hi) return sortedByIntensity[lo].intensity;
    const loVal = sortedByIntensity[lo].intensity;
    const hiVal = sortedByIntensity[hi].intensity;
    return loVal + (idx - lo) * (hiVal - loVal);
  };

  const q1Value = percentile(0.25);
  const q2Value = percentile(0.5);
  const q3Value = percentile(0.75);

  // 找到最接近四分位数强度值的实际数据点
  const findClosestAngle = (targetIntensity) => {
    let closest = pairs[0];
    let minDiff = Math.abs(pairs[0].intensity - targetIntensity);

    for (const pair of pairs) {
      const diff = Math.abs(pair.intensity - targetIntensity);
      if (diff < minDiff) {
        minDiff = diff;
        closest = pair;
      }
    }
    return closest.angle;
  };

  return {
    min: { value: minPair.intensity, angle: minPair.angle },
    max: { value: maxPair.intensity, angle: maxPair.angle },
    q1: { value: q1Value, angle: findClosestAngle(q1Value) },
    q2: { value: q2Value, angle: findClosestAngle(q2Value) },
    q3: { value: q3Value, angle: findClosestAngle(q3Value) }
  };
}

// 计算相似度指标
function calculateSimilarities(result1, result2) {
  if (!result1 || !result2 || !result1.processed || !result2.processed) {
    return {
      cosineSimilarity: null,
      chiSquareTest: null,
      mse: null
    };
  }

  const proc1 = result1.processed;
  const proc2 = result2.processed;

  // 确保两个数据集有相同的角度范围
  const minAngle = Math.max(
    Math.min(...proc1.angles),
    Math.min(...proc2.angles)
  );
  const maxAngle = Math.min(
    Math.max(...proc1.angles),
    Math.max(...proc2.angles)
  );

  // 创建共同的网格
  const commonAngles = [];
  const step = parseFloat(stepInput.value) || 0.01;
  for (let angle = minAngle; angle <= maxAngle; angle += step) {
    commonAngles.push(angle);
  }

  // 插值获取共同网格上的强度值
  const interpolate = (angles, intensities, targetAngles) => {
    const result = [];
    for (const targetAngle of targetAngles) {
      let intensity = 0;
      let found = false;

      for (let i = 0; i < angles.length - 1; i++) {
        if (angles[i] <= targetAngle && targetAngle <= angles[i + 1]) {
          const t = (targetAngle - angles[i]) / (angles[i + 1] - angles[i]);
          intensity = intensities[i] + t * (intensities[i + 1] - intensities[i]);
          found = true;
          break;
        }
      }

      if (!found) {
        // 如果目标角度超出范围，使用最近的值
        if (targetAngle < angles[0]) {
          intensity = intensities[0];
        } else {
          intensity = intensities[intensities.length - 1];
        }
      }

      result.push(intensity);
    }
    return result;
  };

  const intensities1 = interpolate(proc1.angles, proc1.intensities, commonAngles);
  const intensities2 = interpolate(proc2.angles, proc2.intensities, commonAngles);

  // 余弦相似度
  const dotProduct = intensities1.reduce((sum, a, i) => sum + a * intensities2[i], 0);
  const magnitude1 = Math.sqrt(intensities1.reduce((sum, a) => sum + a * a, 0));
  const magnitude2 = Math.sqrt(intensities2.reduce((sum, a) => sum + a * a, 0));
  const cosineSimilarity = magnitude1 > 0 && magnitude2 > 0 ? dotProduct / (magnitude1 * magnitude2) : 0;

  // 卡方检验（简化版本）
  let chiSquare = 0;
  for (let i = 0; i < intensities1.length; i++) {
    const expected = intensities2[i];
    const observed = intensities1[i];
    if (expected > 0) {
      chiSquare += Math.pow(observed - expected, 2) / expected;
    }
  }

  // 均方误差 (MSE)
  const mse = intensities1.reduce((sum, a, i) => sum + Math.pow(a - intensities2[i], 2), 0) / intensities1.length;

  return {
    cosineSimilarity,
    chiSquareTest: chiSquare,
    mse
  };
}

function formatNum(v) {
  if (v == null) return "—";
  if (Math.abs(v) < 1e-4 || Math.abs(v) >= 1e4) return v.toExponential(4);
  return v.toFixed(4);
}

// 更新数据统计栏，显示值和对应的角度
function updateStats(result, datasetNum) {
  const orig = computeStatsWithAngles(result.original.angles, result.original.intensities);
  const proc = computeStatsWithAngles(result.processed.angles, result.processed.intensities);

  function formatStatCell(value, angle) {
    if (value == null || angle == null) return "—";
    return `${formatNum(value)} @ ${formatNum(angle)}°`;
  }

  // 更新原始数据统计
  document.getElementById(`origMax${datasetNum}`).textContent = formatStatCell(orig.max.value, orig.max.angle);
  document.getElementById(`origMin${datasetNum}`).textContent = formatStatCell(orig.min.value, orig.min.angle);
  document.getElementById(`origQ1${datasetNum}`).textContent = formatStatCell(orig.q1.value, orig.q1.angle);
  document.getElementById(`origQ2${datasetNum}`).textContent = formatStatCell(orig.q2.value, orig.q2.angle);
  document.getElementById(`origQ3${datasetNum}`).textContent = formatStatCell(orig.q3.value, orig.q3.angle);

  // 更新处理后数据统计
  document.getElementById(`procMax${datasetNum}`).textContent = formatStatCell(proc.max.value, proc.max.angle);
  document.getElementById(`procMin${datasetNum}`).textContent = formatStatCell(proc.min.value, proc.min.angle);
  document.getElementById(`procQ1${datasetNum}`).textContent = formatStatCell(proc.q1.value, proc.q1.angle);
  document.getElementById(`procQ2${datasetNum}`).textContent = formatStatCell(proc.q2.value, proc.q2.angle);
  document.getElementById(`procQ3${datasetNum}`).textContent = formatStatCell(proc.q3.value, proc.q3.angle);
}

// 更新相似度统计
function updateSimilarityStats() {
  if (lastChartResult1 && lastChartResult2) {
    const similarities = calculateSimilarities(lastChartResult1, lastChartResult2);

    document.getElementById("cosineSimilarity").textContent = formatNum(similarities.cosineSimilarity);
    document.getElementById("chiSquareTest").textContent = formatNum(similarities.chiSquareTest);
    document.getElementById("mseValue").textContent = formatNum(similarities.mse);

    document.getElementById("similaritySection").style.display = "block";
  } else {
    document.getElementById("similaritySection").style.display = "none";
  }
}

// 调用后端 API 处理 XRD（粘贴数据）
async function processXRD(data) {
  const response = await fetch(`${API_BASE}/api/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      data,
      min_angle: parseFloat(minAngleInput.value) || 5,
      max_angle: parseFloat(maxAngleInput.value) || 90,
      step: parseFloat(stepInput.value) || 0.01,
      sigma: parseFloat(sigmaInput.value) || 0.1,
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `请求失败: ${response.status}`);
  }

  return response.json();
}

// 上传 NPY 文件到后端并缓存
async function uploadNpyFile(file, datasetNum) {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE}/api/upload-npy`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `上传失败: ${response.status}`);
  }

  return response.json();
}

// 从已上传的 NPY 文件中处理指定数据组
async function processNpyGroup(filename, groupIndex) {
  const form = new FormData();
  form.append("filename", filename);
  form.append("group_index", groupIndex.toString());
  form.append("min_angle", minAngleInput.value || "5");
  form.append("max_angle", maxAngleInput.value || "90");

  const response = await fetch(`${API_BASE}/api/process-npy-group`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `处理失败: ${response.status}`);
  }

  return response.json();
}

// 在图上标注极值和四分位数的插件
function extremaQuartileLabelPlugin() {
  return {
    id: "extremaQuartileLabels",
    afterDatasetsDraw(chart) {
      const ctx = chart.ctx;
      const font = "11px sans-serif";
      ctx.font = font;
      ctx.fillStyle = "rgba(230, 237, 243, 0.95)";
      ctx.textAlign = "center";

      // 标注最大值和最小值
      const maxMeta = chart.getDatasetMeta(2);
      const minMeta = chart.getDatasetMeta(3);

      if (maxMeta?.data?.[0]) {
        const maxPoint = maxMeta.data[0];
        const maxLabel = chart.data.datasets[2].maxMinLabel || "";
        if (maxLabel) {
          ctx.fillText(maxLabel, maxPoint.x, maxPoint.y - 18);
        }
      }

      if (minMeta?.data?.[0]) {
        const minPoint = minMeta.data[0];
        const minLabel = chart.data.datasets[3].maxMinLabel || "";
        if (minLabel) {
          ctx.fillText(minLabel, minPoint.x, minPoint.y + 24);
        }
      }

      // 标注四分位数
      for (let i = 4; i < Math.min(7, chart.data.datasets.length); i++) {
        const meta = chart.getDatasetMeta(i);
        if (meta?.data?.[0]) {
          const point = meta.data[0];
          const label = chart.data.datasets[i].maxMinLabel || "";
          if (label) {
            ctx.fillText(label, point.x, point.y - 16);
          }
        }
      }
    },
  };
}

// 渲染 XRD 图表
function renderChart(result, chartNum) {
  if (chartNum === 1) {
    lastChartResult1 = result;
  } else {
    lastChartResult2 = result;
  }

  if (typeof Chart === "undefined") {
    alert("Chart.js 未加载成功，请检查网络后刷新页面（F5）重试");
    return;
  }

  const canvasId = `xrdChart${chartNum}`;
  const ctx = document.getElementById(canvasId).getContext("2d");

  // 销毁现有图表
  if (chartNum === 1 && xrdChart1) {
    xrdChart1.destroy();
  } else if (chartNum === 2 && xrdChart2) {
    xrdChart2.destroy();
  }

  const processed = result.processed;
  const original = result.original;
  const useNormalized = chartYModeSelect && chartYModeSelect.value === "normalized";

  let processedY;
  let originalY;
  let yAxisTitle;
  let xMin, xMax, yMin, yMax, xPadding, yPadding;

  if (useNormalized) {
    const maxOrig = Math.max(...original.intensities, 1);
    originalY = original.intensities.map((v) => v / maxOrig);
    processedY = processed.intensities;
    yAxisTitle = "强度 (归一化)";
    const allAngles = [...original.angles, ...processed.angles];
    const allNormY = [...originalY, ...processedY];
    xMin = Math.min(...allAngles);
    xMax = Math.max(...allAngles);
    xPadding = (xMax - xMin) * 0.02 || 1;
    yMin = Math.min(0, ...allNormY);
    yMax = Math.max(...allNormY);
    yPadding = (yMax - yMin) * 0.05 || 0.02;
  } else {
    const maxOrig = Math.max(...original.intensities, 1);
    processedY = processed.intensities.map((v) => v * maxOrig);
    originalY = original.intensities;
    yAxisTitle = "强度";
    const allAngles = [...original.angles, ...processed.angles];
    const allIntensities = [...originalY, ...processedY];
    xMin = Math.min(...allAngles);
    xMax = Math.max(...allAngles);
    yMin = Math.min(0, ...allIntensities);
    yMax = Math.max(...allIntensities);
    xPadding = (xMax - xMin) * 0.02 || 1;
    yPadding = (yMax - yMin) * 0.05 || 1;
  }

  const gridColor = "rgba(139, 148, 158, 0.2)";
  const textColor = "rgba(230, 237, 243, 0.9)";

  // 从展示用的曲线中找全局最大值、最小值（以展宽曲线为主，兼顾原始峰）
  const combinedForExtrema = [
    ...processed.angles.map((a, i) => ({ x: a, y: processedY[i] })),
    ...original.angles.map((a, i) => ({ x: a, y: originalY[i] })),
  ];
  const maxPoint = combinedForExtrema.reduce((a, b) => (a.y >= b.y ? a : b));
  const minPoint = combinedForExtrema.reduce((a, b) => (a.y <= b.y ? a : b));

  // 计算四分位数点（基于处理后的数据）
  const stats = computeStatsWithAngles(processed.angles, processedY);

  // 找到四分位数对应的实际数据点
  const findClosestPoint = (targetAngle, targetValue) => {
    let closest = combinedForExtrema[0];
    let minAngleDiff = Math.abs(combinedForExtrema[0].x - targetAngle);

    for (const point of combinedForExtrema) {
      const angleDiff = Math.abs(point.x - targetAngle);
      if (angleDiff < minAngleDiff) {
        minAngleDiff = angleDiff;
        closest = point;
      }
    }
    return closest;
  };

  const q1Point = stats.q1.angle !== null ? findClosestPoint(stats.q1.angle, stats.q1.value) : null;
  const q2Point = stats.q2.angle !== null ? findClosestPoint(stats.q2.angle, stats.q2.value) : null;
  const q3Point = stats.q3.angle !== null ? findClosestPoint(stats.q3.angle, stats.q3.value) : null;

  const datasets = [
    {
      label: "高斯展宽后",
      data: processed.angles.map((a, i) => ({ x: a, y: processedY[i] })),
      borderColor: "#58a6ff",
      backgroundColor: "rgba(88, 166, 255, 0.1)",
      borderWidth: 2,
      fill: true,
      tension: 0.1,
      pointRadius: 0,
      pointHoverRadius: 2,
    },
    {
      label: "原始峰",
      data: original.angles.map((a, i) => ({ x: a, y: originalY[i] })),
      borderColor: "#f0883e",
      backgroundColor: "rgba(240, 136, 62, 0.3)",
      borderWidth: 1,
      fill: false,
      tension: 0,
      pointRadius: 4,
      pointHoverRadius: 6,
      pointStyle: "circle",
    },
    {
      label: "最大值",
      data: [maxPoint],
      borderColor: "#3fb950",
      backgroundColor: "#3fb950",
      pointRadius: 8,
      pointHoverRadius: 10,
      pointStyle: "triangle",
      order: -1,
      maxMinLabel: `最大值 ${maxPoint.y.toFixed(2)} @ ${maxPoint.x.toFixed(2)}°`,
    },
    {
      label: "最小值",
      data: [minPoint],
      borderColor: "#f85149",
      backgroundColor: "#f85149",
      pointRadius: 10,
      pointHoverRadius: 12,
      pointStyle: "triangle",
      rotation: 180,
      order: -1,
      maxMinLabel: `最小值 ${minPoint.y.toFixed(2)} @ ${minPoint.x.toFixed(2)}°`,
    },
    {
      label: "Q1 (25%)",
      data: q1Point ? [q1Point] : [],
      borderColor: "#ff6b35",
      backgroundColor: "#ff6b35",
      pointRadius: 8,
      pointHoverRadius: 10,
      pointStyle: "rectRot",
      order: -1,
      maxMinLabel: q1Point ? `Q1 ${q1Point.y.toFixed(2)} @ ${q1Point.x.toFixed(2)}°` : "",
    },
    {
      label: "Q2 (中位数)",
      data: q2Point ? [q2Point] : [],
      borderColor: "#f0883e",
      backgroundColor: "#f0883e",
      pointRadius: 8,
      pointHoverRadius: 10,
      pointStyle: "star",
      order: -1,
      maxMinLabel: q2Point ? `中位数 ${q2Point.y.toFixed(2)} @ ${q2Point.x.toFixed(2)}°` : "",
    },
    {
      label: "Q3 (75%)",
      data: q3Point ? [q3Point] : [],
      borderColor: "#ff9f1c",
      backgroundColor: "#ff9f1c",
      pointRadius: 8,
      pointHoverRadius: 10,
      pointStyle: "rectRot",
      order: -1,
      maxMinLabel: q3Point ? `Q3 ${q3Point.y.toFixed(2)} @ ${q3Point.x.toFixed(2)}°` : "",
    },
  ];

  const chart = new Chart(ctx, {
    type: "line",
    data: { datasets },
    plugins: [extremaQuartileLabelPlugin()],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(26, 35, 50, 0.95)",
          titleColor: textColor,
          bodyColor: textColor,
          borderColor: "#30363d",
          borderWidth: 1,
          callbacks: {
            label: (ctx) =>
              `${ctx.dataset.label}: ${ctx.parsed.y != null ? Number(ctx.parsed.y).toFixed(4) : ctx.parsed.y}`,
          },
        },
      },
      scales: {
        x: {
          type: "linear",
          title: {
            display: true,
            text: "2θ (度)",
            color: textColor,
            font: { size: 12 },
          },
          min: xMin - xPadding,
          max: xMax + xPadding,
          grid: { color: gridColor },
          ticks: { color: textColor, maxTicksLimit: 12 },
        },
        y: {
          title: {
            display: true,
            text: yAxisTitle,
            color: textColor,
            font: { size: 12 },
          },
          min: yMin - yPadding,
          max: yMax + yPadding,
          grid: { color: gridColor },
          ticks: { color: textColor },
        },
      },
    },
  });

  if (chartNum === 1) {
    xrdChart1 = chart;
  } else {
    xrdChart2 = chart;
  }
}

// 处理单个数据集
async function handleProcessDataset(datasetNum) {
  const mode = getActiveInputTab(datasetNum);
  const inputTextArea = datasetNum === 1 ? dataInput1 : dataInput2;
  const groupIndexInput = datasetNum === 1 ? groupIndexInput1 : groupIndexInput2;
  const uploadedNpyFile = datasetNum === 1 ? uploadedNpyFile1 : uploadedNpyFile2;

  console.log(`处理数据集 ${datasetNum}, 模式: ${mode}, 文件状态:`, uploadedNpyFile);

  // 处理 NPY 文件模式
  if (mode === `npy${datasetNum}`) {
    if (!uploadedNpyFile) {
      console.log(`数据集 ${datasetNum} NPY 文件未找到`);
      alert(`请先上传并选择数据集 ${datasetNum} 的 NPY 文件`);
      return;
    }

    // 额外检查：确保文件信息完整
    if (!uploadedNpyFile.filename || !uploadedNpyFile.totalGroups) {
      alert(`数据集 ${datasetNum} 的 NPY 文件信息不完整，请重新上传`);
      // 重置文件状态
      if (datasetNum === 1) {
        uploadedNpyFile1 = null;
      } else {
        uploadedNpyFile2 = null;
      }
      return;
    }

    const groupIndex = parseInt(groupIndexInput.value) || 0;
    if (groupIndex < 0 || groupIndex >= uploadedNpyFile.totalGroups) {
      alert(`数据组索引超出范围，请输入 0-${uploadedNpyFile.totalGroups - 1} 之间的数字`);
      return;
    }

    try {
      console.log(`处理数据集 ${datasetNum}, 文件名: ${uploadedNpyFile.filename}, 组索引: ${groupIndex}`);
      const result = await processNpyGroup(uploadedNpyFile.filename, groupIndex);
      console.log(`数据集 ${datasetNum} 处理成功:`, result);
      renderChart(result, datasetNum);
      updateStats(result, datasetNum);
      updateSimilarityStats();
    } catch (err) {
      alert(`处理失败: ${err.message}\n\n请确保后端服务已启动 (python main.py 或 uvicorn main:app)`);
    }
    return; // 重要：处理完 NPY 后直接返回，不再执行下面的文本处理逻辑
  }

  // 处理文本输入模式
  const text = inputTextArea.value.trim();
  if (!text) {
    alert(`请输入数据集 ${datasetNum} 的 XRD 数据（每行：角度 强度）或切换到「上传 NPY 文件」`);
    return;
  }

  const data = parseXRDInput(text);
  if (data.length === 0) {
    alert("无法解析有效数据，请检查格式（每行：角度 强度，空格或制表符分隔）");
    return;
  }

  try {
    const result = await processXRD(data);
    renderChart(result, datasetNum);
    updateStats(result, datasetNum);
    updateSimilarityStats();
  } catch (err) {
    alert(`处理失败: ${err.message}\n\n请确保后端服务已启动 (python main.py 或 uvicorn main:app)`);
  }
}

// 处理按钮点击
async function handleProcess() {
  processBtn.disabled = true;
  processBtn.textContent = "处理中...";

  try {
    await Promise.all([
      handleProcessDataset(1),
      handleProcessDataset(2)
    ]);
  } finally {
    processBtn.disabled = false;
    processBtn.textContent = "处理并可视化";
  }
}

// 加载示例数据
function handleLoadSample(datasetNum) {
  const inputTextArea = datasetNum === 1 ? dataInput1 : dataInput2;
  const sampleData = datasetNum === 1 ? SAMPLE_DATA_1 : SAMPLE_DATA_2;
  inputTextArea.value = sampleData;
  document.querySelector(`.dataset-section:nth-child(${datasetNum}) [data-tab="paste${datasetNum}"]`).click();
}

// Tab 切换
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    const datasetSection = tab.closest('.dataset-section');
    const datasetNum = datasetSection ? Array.from(document.querySelectorAll('.dataset-section')).indexOf(datasetSection) + 1 : 1;

    // 移除当前数据集的所有 active 状态
    const tabs = datasetSection.querySelectorAll(".tab");
    const contents = datasetSection.querySelectorAll(".tab-content");

    tabs.forEach((t) => t.classList.remove("active"));
    contents.forEach((c) => c.classList.remove("active"));

    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});

// NPY 文件选择后更新标签并上传文件
function setupNpyFileInput(fileInput, fileLabel, fileInfo, fileDetails, groupIndexInput, datasetNum) {
  fileInput.addEventListener("change", async () => {
    const wrap = fileInput.closest(".file-input-wrap");
    if (fileInput.files && fileInput.files[0]) {
      const file = fileInput.files[0];
      fileLabel.textContent = file.name;
      wrap.classList.add("has-file");

      try {
        // 上传文件到后端
        console.log(`上传 NPY 文件: ${file.name} (数据集 ${datasetNum})`);
        const result = await uploadNpyFile(file, datasetNum);
        console.log(`上传成功，后端返回:`, result);

        const uploadedFile = {
          filename: result.filename,
          totalGroups: result.total_groups,
          gridPoints: result.grid_points
        };

        if (datasetNum === 1) {
          uploadedNpyFile1 = uploadedFile;
          console.log(`数据集 1 文件已缓存:`, uploadedNpyFile1);
        } else {
          uploadedNpyFile2 = uploadedFile;
          console.log(`数据集 2 文件已缓存:`, uploadedNpyFile2);
        }

        // 显示文件信息
        fileDetails.textContent = `已加载: ${result.total_groups} 组数据，每组 ${result.grid_points} 个网格点`;
        fileInfo.style.display = "block";

        // 设置组选择器的最大值
        groupIndexInput.max = result.total_groups - 1;
        groupIndexInput.value = "0";

        // ===== 修复标签切换问题 =====
        setTimeout(() => {
          console.log(`开始切换数据集 ${datasetNum} 到 NPY 标签`);
          
          // 使用 querySelectorAll 获取所有 section
          const datasetSections = document.querySelectorAll('.dataset-section');
          
          if (datasetSections.length < datasetNum) {
            console.error(`找不到数据集 ${datasetNum} 的 section，总共有 ${datasetSections.length} 个 section`);
            return;
          }
          
          const section = datasetSections[datasetNum - 1]; // 转换为 0-based 索引
          console.log(`找到数据集 ${datasetNum} 的 section`);
          
          if (section) {
            // 获取当前数据集的所有标签
            const tabs = section.querySelectorAll('.method-tabs .tab');
            const contents = section.querySelectorAll('.tab-content');
            
            console.log(`找到 ${tabs.length} 个标签:`, Array.from(tabs).map(t => t.dataset.tab));
            console.log(`找到 ${contents.length} 个内容:`, Array.from(contents).map(c => c.id));
            
            // 移除所有 active 状态
            tabs.forEach(tab => {
              tab.classList.remove('active');
              console.log(`移除标签 ${tab.dataset.tab} 的 active 状态`);
            });
            
            contents.forEach(content => {
              content.classList.remove('active');
              console.log(`移除内容 ${content.id} 的 active 状态`);
            });
            
            // 激活 NPY 标签 - 使用正确的 data-tab 值
            const targetTabId = `npy${datasetNum}`;
            const targetContentId = `npy${datasetNum}`;
            
            // 找到对应的标签和内容
            const targetTab = Array.from(tabs).find(tab => tab.dataset.tab === targetTabId);
            const targetContent = document.getElementById(targetContentId);
            
            if (targetTab && targetContent) {
              console.log(`激活标签: ${targetTabId}, 内容: ${targetContentId}`);
              targetTab.classList.add('active');
              targetContent.classList.add('active');
              
              // 验证
              console.log(`激活后标签状态:`, targetTab.classList.contains('active'));
              console.log(`激活后内容状态:`, targetContent.classList.contains('active'));
              
              // 验证 getActiveInputTab 函数
              setTimeout(() => {
                console.log(`验证 getActiveInputTab(${datasetNum}) 返回值:`, getActiveInputTab(datasetNum));
              }, 100);
            } else {
              console.error(`找不到标签或内容:`, {
                targetTab: targetTab ? '找到' : '未找到',
                targetContent: targetContent ? '找到' : '未找到',
                availableTabs: Array.from(tabs).map(t => t.dataset.tab),
                availableContentIds: Array.from(contents).map(c => c.id)
              });
            }
          } else {
            console.error(`找不到数据集 ${datasetNum} 的 section`);
          }
        }, 200);

      } catch (error) {
        alert(`文件上传失败: ${error.message}`);
        fileInfo.style.display = "none";
        if (datasetNum === 1) {
          uploadedNpyFile1 = null;
        } else {
          uploadedNpyFile2 = null;
        }
      }
    } else {
      fileLabel.textContent = "选择 .npy 文件";
      wrap.classList.remove("has-file");
      fileInfo.style.display = "none";
      if (datasetNum === 1) {
        uploadedNpyFile1 = null;
      } else {
        uploadedNpyFile2 = null;
      }
    }
  });
}

// 设置文件输入
setupNpyFileInput(npyFileInput1, npyFileLabel1, npyFileInfo1, npyFileDetails1, groupIndexInput1, 1);
setupNpyFileInput(npyFileInput2, npyFileLabel2, npyFileInfo2, npyFileDetails2, groupIndexInput2, 2);

processBtn.addEventListener("click", handleProcess);
loadSampleBtn1.addEventListener("click", () => handleLoadSample(1));
loadSampleBtn2.addEventListener("click", () => handleLoadSample(2));
refreshGroupBtn1.addEventListener("click", () => handleProcessDataset(1));
refreshGroupBtn2.addEventListener("click", () => handleProcessDataset(2));

if (chartYModeSelect) {
  chartYModeSelect.addEventListener("change", () => {
    if (lastChartResult1) renderChart(lastChartResult1, 1);
    if (lastChartResult2) renderChart(lastChartResult2, 2);
  });
}

// 调试函数：检查文件状态
function checkFileStatus() {
  console.log("=== 文件状态检查 ===");
  console.log("数据集 1 文件:", uploadedNpyFile1);
  console.log("数据集 2 文件:", uploadedNpyFile2);
  console.log("数据集 1 当前标签:", getActiveInputTab(1));
  console.log("数据集 2 当前标签:", getActiveInputTab(2));
}

// 添加调试按钮（开发时使用）
// setTimeout(() => {
//   const debugBtn = document.createElement('button');
//   debugBtn.textContent = '检查文件状态';
//   debugBtn.onclick = checkFileStatus;
//   debugBtn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:9999;';
//   document.body.appendChild(debugBtn);
// }, 1000);