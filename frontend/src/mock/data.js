// =============== Mock User Data ===============
export const mockUsers = [
  { id: 1, username: 'admin', email: 'admin@ustc.edu.cn', password: 'admin123', role: 'admin', nickname: '管理员', phone: '13800138000', avatar: '', createTime: '2024-01-01' },
  { id: 2, username: 'user1', email: 'user1@ustc.edu.cn', password: 'user123', role: 'user', nickname: '用户1', phone: '13800138001', avatar: '', createTime: '2024-02-01' },
  { id: 3, username: 'researcher', email: 'researcher@ustc.edu.cn', password: 'test123', role: 'user', nickname: '研究人员', phone: '13800138002', avatar: '', createTime: '2024-03-01' }
]

// =============== Mock News Data ===============
export const mockNews = [
  { id: 1, title: '精准化学数据平台正式上线运行', content: '<p>经过数年的建设与测试，精准化学数据平台（PIChemData）于近日正式上线运行。该平台集成了大量的化学分子数据、材料数据和文献数据，为广大科研工作者提供便捷的数据检索和分析服务。</p><p>平台目前收录了超过10万条分子数据、5万条材料数据以及相关文献信息。用户可以通过平台进行分子结构搜索、相似性分析、材料性质查询等多种操作。</p>', author: '管理员', createTime: '2025-12-01 10:00:00', summary: '精准化学数据平台正式上线运行，集成大量化学数据资源。' },
  { id: 2, title: '平台新增AI智能助手功能', content: '<p>为进一步提升用户体验，精准化学数据平台近日推出了AI智能助手功能。用户可以通过自然语言输入，快速查询化学元素信息、分子结构、材料性质等数据。</p><p>智能助手支持中英文双语交互，能够理解复杂的化学查询需求，并给出准确的数据反馈。该功能基于大语言模型技术开发，将持续优化和改进。</p>', author: '产品团队', createTime: '2025-12-15 14:30:00', summary: '新增AI智能助手，支持自然语言查询化学数据。' },
  { id: 3, title: '数据更新：新增过渡金属催化剂数据集', content: '<p>平台最新收录了一批过渡金属催化剂数据集，涵盖Fe、Co、Ni、Cu、Pd、Pt等多种过渡金属的催化体系。数据来源于国内外高水平期刊论文和实验测量结果。</p><p>该数据集包含催化剂结构信息、反应条件、催化性能指标等详细信息，可用于机器学习模型训练和催化机理研究。</p>', author: '数据团队', createTime: '2025-12-28 09:00:00', summary: '新增过渡金属催化剂数据集。' },
  { id: 4, title: 'API接口更新公告', content: '<p>精准化学数据平台API接口已升级至v1.2版本，新增分子相似性搜索接口、材料性质批量查询接口等功能。请各位开发者及时更新您的应用程序。</p><p>详细接口文档请参见API信息页面。</p>', author: '技术团队', createTime: '2026-01-10 16:00:00', summary: 'API接口升级至v1.2，新增多项功能。' },
  { id: 5, title: '平台获得国家自然科学基金资助', content: '<p>精准化学数据平台建设项目获得国家自然科学基金面上项目资助。项目将重点建设高质量化学数据的标准化收集、管理和共享机制。</p>', author: '项目组', createTime: '2026-02-20 11:00:00', summary: '获得国家自然科学基金资助。' }
]

// =============== Mock Announcements ===============
export const mockAnnouncements = [
  { id: 1, title: '系统维护通知：2026年1月15日凌晨2:00-6:00', content: '<p>尊敬的平台用户：</p><p>为提升系统性能和稳定性，平台将于2026年1月15日凌晨2:00至6:00进行系统维护升级。维护期间平台将暂停服务，给您带来的不便敬请谅解。</p><p>如有紧急需求，请联系管理员邮箱：admin@ustc.edu.cn</p>', author: '系统管理员', createTime: '2026-01-10', importance: 'high' },
  { id: 2, title: '关于数据入库标准的补充说明', content: '<p>为提高平台数据质量，现将数据入库标准补充说明如下：</p><p>1. 所有上传数据须包含完整的元数据信息<br>2. 分子数据须提供SMILES或InChI标识符<br>3. 计算数据须注明计算方法和基组信息</p>', author: '数据管理组', createTime: '2026-01-20', importance: 'medium' },
  { id: 3, title: '2026年春节假期服务安排', content: '<p>根据学校统一安排，平台运营团队春节期间（2026年2月17日-2月25日）将采用在线值班方式。期间平台正常运行，但数据处理和审核可能会有延迟。</p>', author: '运营团队', createTime: '2026-02-10', importance: 'low' },
  { id: 4, title: '化学数据标准研讨会通知', content: '<p>兹定于2026年3月15日举办"化学数据标准化与共享"在线研讨会，欢迎各位同仁参加。</p><p>会议日程及报名方式请参见附件。</p>', author: '学术委员会', createTime: '2026-03-01', importance: 'medium' }
]

// =============== Mock Molecule Data ===============
export const mockMolecules = [
  { id: 1, formula: 'H2O', smiles: 'O', inchi: 'InChI=1S/H2O/h1H2', mass: 18.015, volume: 18.07, type: '无机小分子', tags: ['水', '溶剂', '无机'], charge: 0, spin: 1, atoms: ['H', 'H', 'O'], bonds: [[0, 2, 1], [1, 2, 1]], createTime: '2025-12-01' },
  { id: 2, formula: 'CH4', smiles: 'C', inchi: 'InChI=1S/CH4/h1H4', mass: 16.043, volume: 24.45, type: '有机小分子', tags: ['甲烷', '烷烃', '天然气'], charge: 0, spin: 1, atoms: ['C', 'H', 'H', 'H', 'H'], bonds: [[0, 1, 1], [0, 2, 1], [0, 3, 1], [0, 4, 1]], createTime: '2025-12-01' },
  { id: 3, formula: 'C2H5OH', smiles: 'CCO', inchi: 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3', mass: 46.069, volume: 58.37, type: '有机小分子', tags: ['乙醇', '醇类', '溶剂'], charge: 0, spin: 1, atoms: ['C', 'C', 'O', 'H', 'H', 'H', 'H', 'H', 'H'], bonds: [[0, 1, 1], [1, 2, 1], [0, 3, 1], [0, 4, 1], [0, 5, 1], [1, 6, 1], [1, 7, 1], [2, 8, 1]], createTime: '2025-12-02' },
  { id: 4, formula: 'C6H6', smiles: 'c1ccccc1', inchi: 'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H', mass: 78.114, volume: 89.24, type: '芳香族化合物', tags: ['苯', '芳香族', '有机溶剂'], charge: 0, spin: 1, atoms: ['C', 'C', 'C', 'C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H'], bonds: [[0, 1, 2], [1, 2, 1], [2, 3, 2], [3, 4, 1], [4, 5, 2], [5, 0, 1], [0, 6, 1], [1, 7, 1], [2, 8, 1], [3, 9, 1], [4, 10, 1], [5, 11, 1]], createTime: '2025-12-02' },
  { id: 5, formula: 'CO2', smiles: 'O=C=O', inchi: 'InChI=1S/CO2/c2-1-3', mass: 44.009, volume: 29.69, type: '无机小分子', tags: ['二氧化碳', '温室气体', '无机'], charge: 0, spin: 1, atoms: ['C', 'O', 'O'], bonds: [[0, 1, 2], [0, 2, 2]], createTime: '2025-12-03' },
  { id: 6, formula: 'NH3', smiles: 'N', inchi: 'InChI=1S/H3N/h1H3', mass: 17.031, volume: 22.41, type: '无机小分子', tags: ['氨', '无机', '碱'], charge: 0, spin: 1, atoms: ['N', 'H', 'H', 'H'], bonds: [[0, 1, 1], [0, 2, 1], [0, 3, 1]], createTime: '2025-12-03' },
  { id: 7, formula: 'CH3COOH', smiles: 'CC(=O)O', inchi: 'InChI=1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)', mass: 60.052, volume: 57.06, type: '有机小分子', tags: ['乙酸', '羧酸', '有机酸'], charge: 0, spin: 1, atoms: ['C', 'C', 'O', 'O', 'H', 'H', 'H', 'H'], bonds: [[0, 1, 1], [1, 2, 2], [1, 3, 1], [0, 4, 1], [0, 5, 1], [0, 6, 1], [3, 7, 1]], createTime: '2025-12-04' },
  { id: 8, formula: 'C3H8O', smiles: 'CCCO', inchi: 'InChI=1S/C3H8O/c1-2-3-4/h4H,2-3H2,1H3', mass: 60.096, volume: 75.17, type: '有机小分子', tags: ['正丙醇', '醇类', '溶剂'], charge: 0, spin: 1, createTime: '2025-12-04' },
  { id: 9, formula: 'NaCl', smiles: '[Na+].[Cl-]', inchi: 'InChI=1S/ClH.Na/h1H;/q;+1/p-1', mass: 58.44, volume: 27.02, type: '无机盐', tags: ['氯化钠', '盐', '无机'], charge: 0, spin: 1, createTime: '2025-12-05' },
  { id: 10, formula: 'C2H4', smiles: 'C=C', inchi: 'InChI=1S/C2H4/c1-2/h1-2H2', mass: 28.054, volume: 22.41, type: '烯烃', tags: ['乙烯', '烯烃', '石化原料'], charge: 0, spin: 1, createTime: '2025-12-05' },
  { id: 11, formula: 'H2SO4', smiles: 'OS(=O)(=O)O', inchi: 'InChI=1S/H2O4S/c1-5(2,3)4/h(H2,1,2,3,4)', mass: 98.079, volume: 53.62, type: '无机酸', tags: ['硫酸', '强酸', '无机酸'], charge: 0, spin: 1, createTime: '2025-12-06' },
  { id: 12, formula: 'C7H8', smiles: 'Cc1ccccc1', inchi: 'InChI=1S/C7H8/c1-7-5-3-2-4-6-7/h2-6H,1H3', mass: 92.141, volume: 106.29, type: '芳香族化合物', tags: ['甲苯', '芳香族', '溶剂'], charge: 0, spin: 1, createTime: '2025-12-06' }
]

// =============== Mock Materials Data ===============
export const mockMaterials = [
  { id: 1, name: 'Cu(111)表面', formula: 'Cu', type: '金属表面', tags: ['铜', '表面', '催化', '过渡金属'], bandGap: null, latticeConstant: 3.615, crystalSystem: '面心立方', spaceGroup: 'Fm-3m', createTime: '2025-12-01' },
  { id: 2, name: 'TiO2锐钛矿', formula: 'TiO2', type: '金属氧化物', tags: ['二氧化钛', '光催化', '半导体'], bandGap: 3.2, latticeConstant: 3.785, crystalSystem: '四方', spaceGroup: 'I41/amd', createTime: '2025-12-02' },
  { id: 3, name: '石墨烯', formula: 'C', type: '二维材料', tags: ['石墨烯', '二维材料', '碳材料'], bandGap: 0, latticeConstant: 2.46, crystalSystem: '六方', spaceGroup: 'P6/mmm', createTime: '2025-12-03' },
  { id: 4, name: 'ZnO纤锌矿', formula: 'ZnO', type: '金属氧化物', tags: ['氧化锌', '半导体', '压电材料'], bandGap: 3.37, latticeConstant: 3.249, crystalSystem: '六方', spaceGroup: 'P63mc', createTime: '2025-12-04' },
  { id: 5, name: 'Fe2O3赤铁矿', formula: 'Fe2O3', type: '金属氧化物', tags: ['氧化铁', '磁性材料', '催化剂'], bandGap: 2.2, latticeConstant: 5.036, crystalSystem: '六方', spaceGroup: 'R-3c', createTime: '2025-12-05' },
  { id: 6, name: 'Pt(111)表面', formula: 'Pt', type: '金属表面', tags: ['铂', '表面', '催化', '贵金属'], bandGap: null, latticeConstant: 3.924, crystalSystem: '面心立方', spaceGroup: 'Fm-3m', createTime: '2025-12-06' },
  { id: 7, name: 'MoS2单层', formula: 'MoS2', type: '二维材料', tags: ['二硫化钼', '二维材料', 'TMD'], bandGap: 1.8, latticeConstant: 3.16, crystalSystem: '六方', spaceGroup: 'P63/mmc', createTime: '2025-12-07' },
  { id: 8, name: 'Al2O3刚玉', formula: 'Al2O3', type: '金属氧化物', tags: ['氧化铝', '陶瓷', '载体'], bandGap: 8.7, latticeConstant: 4.759, crystalSystem: '三方', spaceGroup: 'R-3c', createTime: '2025-12-08' }
]

// =============== Mock Literature Data ===============
export const mockLiterature = [
  { id: 1, doi: '10.1021/jacs.5b01234', title: 'Density Functional Theory Study of CO2 Reduction on Transition Metal Surfaces', authors: 'Zhang, L.; Wang, H.; Li, J.', journal: 'Journal of the American Chemical Society', year: 2025, volume: '137', issue: '15', pages: '5123-5130', abstract: 'A comprehensive DFT study of CO2 reduction reaction mechanisms on various transition metal surfaces, including Cu, Ag, Au, and Pt.', keywords: ['CO2 reduction', 'DFT', 'transition metals', 'catalysis'], tags: ['催化', 'DFT计算', '过渡金属'] },
  { id: 2, doi: '10.1038/s41563-024-01789-0', title: 'Machine Learning Accelerated Discovery of Novel Perovskite Materials for Solar Cells', authors: 'Chen, X.; Liu, Y.; Wang, Z.; et al.', journal: 'Nature Materials', year: 2025, volume: '24', issue: '3', pages: '301-310', abstract: 'Using machine learning models trained on high-throughput DFT calculations to screen novel perovskite compositions for photovoltaic applications.', keywords: ['machine learning', 'perovskite', 'solar cells', 'high-throughput screening'], tags: ['机器学习', '钙钛矿', '太阳能电池'] },
  { id: 3, doi: '10.1002/anie.2024112345', title: 'Single-Atom Catalysts for Efficient Nitrogen Reduction Reaction', authors: 'Wang, F.; Zhang, Q.; Li, M.', journal: 'Angewandte Chemie International Edition', year: 2025, volume: '64', issue: '8', pages: 'e2024112345', abstract: 'Design and synthesis of single-atom catalysts supported on N-doped carbon for electrochemical nitrogen reduction to ammonia.', keywords: ['single-atom catalyst', 'nitrogen reduction', 'electrocatalysis'], tags: ['单原子催化', '氮还原', '电催化'] },
  { id: 4, doi: '10.1126/science.ade1234', title: 'Direct Observation of Chemical Reaction Dynamics at Single-Molecule Level', authors: 'Johnson, R.; Smith, A.; Brown, T.', journal: 'Science', year: 2026, volume: '381', issue: '6654', pages: '456-460', abstract: 'Using advanced microscopy techniques to observe individual chemical reaction events in real-time at the single-molecule level.', keywords: ['single-molecule', 'reaction dynamics', 'microscopy'], tags: ['单分子', '反应动力学', '显微技术'] },
  { id: 5, doi: '10.1039/D4SC05678-9', title: 'Data-Driven Design of Metal-Organic Frameworks for Gas Separation', authors: 'Li, H.; Kim, J.; Park, S.', journal: 'Chemical Science', year: 2025, volume: '16', issue: '12', pages: '2890-2905', abstract: 'A data-driven approach combining molecular simulation and machine learning for screening MOFs for CO2/N2 and CO2/CH4 separation.', keywords: ['MOF', 'gas separation', 'machine learning', 'molecular simulation'], tags: ['MOF', '气体分离', '机器学习'] }
]

// =============== Mock Tags ===============
export const mockMoleculeTags = [
  { id: 1, name: '溶剂', count: 45, category: '应用' },
  { id: 2, name: '催化剂', count: 38, category: '应用' },
  { id: 3, name: '有机', count: 120, category: '类型' },
  { id: 4, name: '无机', count: 89, category: '类型' },
  { id: 5, name: '芳香族', count: 56, category: '结构' },
  { id: 6, name: '烷烃', count: 34, category: '结构' },
  { id: 7, name: '烯烃', count: 28, category: '结构' },
  { id: 8, name: '醇类', count: 42, category: '官能团' },
  { id: 9, name: '羧酸', count: 25, category: '官能团' },
  { id: 10, name: '过渡金属', count: 67, category: '元素' },
  { id: 11, name: '半导体', count: 30, category: '性质' },
  { id: 12, name: '二维材料', count: 22, category: '结构' }
]

export const mockMaterialTags = [
  { id: 1, name: '催化', count: 55, category: '应用' },
  { id: 2, name: '光催化', count: 28, category: '应用' },
  { id: 3, name: '半导体', count: 35, category: '性质' },
  { id: 4, name: '金属', count: 80, category: '类型' },
  { id: 5, name: '氧化物', count: 60, category: '类型' },
  { id: 6, name: '二维材料', count: 25, category: '结构' },
  { id: 7, name: '表面', count: 40, category: '结构' },
  { id: 8, name: '磁性材料', count: 18, category: '性质' },
  { id: 9, name: '钙钛矿', count: 15, category: '结构' },
  { id: 10, name: '陶瓷', count: 20, category: '类型' }
]

// =============== Mock API Definitions ===============
export const mockApiServices = [
  {
    name: 'molecule',
    label: '分子数据服务',
    description: '提供化学分子的查询、搜索和结构信息获取功能',
    apis: [
      { name: 'GET /molecule/list', method: 'GET', path: '/api/v1/molecule/list', desc: '获取分子列表', params: 'page, size, keyword, type', response: '{ code: 200, data: { result: [...], page: { size, current, total } } }' },
      { name: 'GET /molecule/detail', method: 'GET', path: '/api/v1/molecule/detail', desc: '获取分子详情', params: 'id', response: '{ code: 200, data: { id, formula, smiles, inchi, mass, volume, ... } }' },
      { name: 'GET /molecule/search', method: 'GET', path: '/api/v1/molecule/search', desc: '分子搜索', params: 'keyword, formula, smiles, type', response: '{ code: 200, data: { result: [...] } }' },
      { name: 'POST /molecule/similarity', method: 'POST', path: '/api/v1/molecule/similarity', desc: '分子相似性搜索', params: '{ smiles, type: "2d"|"3d", threshold }', response: '{ code: 200, data: { result: [{ id, formula, similarity }] } }' }
    ]
  },
  {
    name: 'materials',
    label: '材料数据服务',
    description: '提供材料数据的查询、搜索和性质信息获取功能',
    apis: [
      { name: 'GET /materials/list', method: 'GET', path: '/api/v1/materials/list', desc: '获取材料列表', params: 'page, size, keyword, type', response: '{ code: 200, data: { result: [...], page: { size, current, total } } }' },
      { name: 'GET /materials/detail', method: 'GET', path: '/api/v1/materials/detail', desc: '获取材料详情', params: 'id', response: '{ code: 200, data: { id, name, formula, type, ... } }' }
    ]
  },
  {
    name: 'literature',
    label: '文献数据服务',
    description: '提供科研文献的检索和详情获取功能',
    apis: [
      { name: 'GET /literature/list', method: 'GET', path: '/api/v1/literature/list', desc: '获取文献列表', params: 'page, size, keyword, doi', response: '{ code: 200, data: { result: [...], page: { size, current, total } } }' },
      { name: 'GET /literature/detail', method: 'GET', path: '/api/v1/literature/detail', desc: '获取文献详情', params: 'id', response: '{ code: 200, data: { id, doi, title, authors, ... } }' }
    ]
  }
]

// =============== Mock Audit Logs ===============
export const mockAuditLogs = [
  { id: 1, userId: 1, username: 'admin', action: '登录', resource: '系统', detail: '用户登录成功', ip: '202.38.64.1', time: '2026-01-15 08:30:00' },
  { id: 2, userId: 2, username: 'user1', action: '查询', resource: '分子数据', detail: '搜索关键词：H2O', ip: '202.38.64.2', time: '2026-01-15 09:15:00' },
  { id: 3, userId: 1, username: 'admin', action: '创建', resource: '元数据', detail: '创建元数据字段：计算方法', ip: '202.38.64.1', time: '2026-01-15 10:00:00' },
  { id: 4, userId: 3, username: 'researcher', action: '上传', resource: '数据', detail: '上传分子数据文件：dataset_2024.json', ip: '202.38.64.3', time: '2026-01-15 11:20:00' },
  { id: 5, userId: 2, username: 'user1', action: '下载', resource: 'API', detail: '通过API下载分子列表', ip: '202.38.64.2', time: '2026-01-15 14:45:00' },
  { id: 6, userId: 1, username: 'admin', action: '删除', resource: '标签', detail: '删除标签：废弃标签', ip: '202.38.64.1', time: '2026-01-15 16:00:00' },
  { id: 7, userId: 3, username: 'researcher', action: '修改', resource: '账户', detail: '修改个人信息', ip: '202.38.64.3', time: '2026-01-15 17:30:00' }
]

// =============== Mock Metadata ===============
export const mockMetadata = [
  { id: 1, fieldEn: 'calculation_method', fieldZh: '计算方法', type: 'string', required: true, description: '使用的计算方法和基组' },
  { id: 2, fieldEn: 'potential_energy', fieldZh: '势能', type: 'float', required: false, description: '体系总势能 (eV)' },
  { id: 3, fieldEn: 'temperature', fieldZh: '温度', type: 'float', required: false, description: '计算/实验温度 (K)' },
  { id: 4, fieldEn: 'pressure', fieldZh: '压力', type: 'float', required: false, description: '计算/实验压力 (Pa)' },
  { id: 5, fieldEn: 'basis_set', fieldZh: '基组', type: 'string', required: false, description: '计算使用的基组' },
  { id: 6, fieldEn: 'functional', fieldZh: '泛函', type: 'string', required: false, description: 'DFT计算使用的泛函' }
]

// =============== Mock Spectrum Data ===============
// Keyed by pic_id (matches molecule.id)
export const mockSpectrum = [
  {
    picId: 1,
    spectra: [
      {
        id: 'spec-1-ir',
        type: 'IR',
        name: 'H₂O FTIR Spectrum',
        instrument: 'Bruker VERTEX 70',
        conditions: 'KBr pellet, 400-4000 cm⁻¹, RT',
        xLabel: 'Wavenumber (cm⁻¹)',
        yLabel: 'Transmittance (%)',
        peaks: [
          { x: 3450, y: 82, label: 'O-H stretch (sym)' },
          { x: 1640, y: 68, label: 'H-O-H bend' },
          { x: 3756, y: 88, label: 'O-H stretch (asym)' },
          { x: 660, y: 42, label: 'O-H libration' }
        ],
        dataPoints: [
          [400, 95], [600, 88], [800, 78], [1000, 65], [1200, 72],
          [1400, 80], [1600, 68], [1800, 85], [2000, 90], [2200, 92],
          [2400, 93], [2600, 94], [2800, 95], [3000, 90], [3200, 85],
          [3400, 70], [3600, 60], [3756, 88], [3900, 45], [4000, 40]
        ]
      },
      {
        id: 'spec-1-nmr',
        type: 'NMR',
        name: '¹H NMR Spectrum of H₂O',
        instrument: 'Bruker AVANCE III 400',
        conditions: 'D₂O, 400 MHz, 298K',
        xLabel: 'Chemical Shift (ppm)',
        yLabel: 'Intensity',
        peaks: [
          { x: 4.79, y: 90, label: 'HDO (solvent)' }
        ],
        dataPoints: [
          [0, 5], [0.5, 6], [1, 8], [1.5, 9], [2, 11],
          [2.5, 10], [3, 13], [3.5, 15], [4, 22], [4.3, 40],
          [4.5, 60], [4.7, 85], [4.79, 90], [4.9, 55], [5, 35],
          [5.5, 18], [6, 12], [7, 8], [8, 5], [9, 3], [10, 2]
        ]
      }
    ]
  },
  {
    picId: 3,
    spectra: [
      {
        id: 'spec-3-ir',
        type: 'IR',
        name: 'Ethanol FTIR Spectrum',
        instrument: 'Thermo Nicolet iS50',
        conditions: 'KBr pellet, 400-4000 cm⁻¹, RT',
        xLabel: 'Wavenumber (cm⁻¹)',
        yLabel: 'Transmittance (%)',
        peaks: [
          { x: 3340, y: 75, label: 'O-H stretch' },
          { x: 2974, y: 82, label: 'C-H stretch (asym)' },
          { x: 2880, y: 85, label: 'C-H stretch (sym)' },
          { x: 1050, y: 60, label: 'C-O stretch' }
        ],
        dataPoints: [
          [400, 92], [600, 85], [800, 72], [1000, 62], [1050, 60],
          [1200, 70], [1400, 78], [1600, 88], [1800, 90], [2000, 92],
          [2200, 94], [2400, 93], [2600, 88], [2800, 85], [2880, 85],
          [2974, 82], [3100, 78], [3340, 75], [3500, 60], [3700, 45], [4000, 38]
        ]
      },
      {
        id: 'spec-3-ms',
        type: 'MS',
        name: 'Ethanol EI Mass Spectrum',
        instrument: 'Agilent 5977B GC/MSD',
        conditions: 'EI 70eV, m/z 10-100',
        xLabel: 'm/z',
        yLabel: 'Relative Abundance (%)',
        peaks: [
          { x: 31, y: 100, label: '[CH₂OH]⁺' },
          { x: 45, y: 52, label: '[C₂H₅O]⁺' },
          { x: 46, y: 18, label: '[M]⁺·' },
          { x: 27, y: 35, label: '[C₂H₃]⁺' },
          { x: 29, y: 28, label: '[C₂H₅]⁺' }
        ],
        dataPoints: [
          [10, 2], [15, 10], [18, 8], [20, 5], [25, 15],
          [27, 35], [29, 28], [31, 100], [35, 8], [40, 12],
          [43, 20], [45, 52], [46, 18], [47, 3], [50, 5],
          [55, 3], [60, 1], [70, 1], [80, 0], [100, 0]
        ]
      }
    ]
  },
  {
    picId: 4,
    spectra: [
      {
        id: 'spec-4-ir',
        type: 'IR',
        name: 'Benzene FTIR Spectrum',
        instrument: 'Bruker VERTEX 70',
        conditions: 'KBr pellet, 400-4000 cm⁻¹, RT',
        xLabel: 'Wavenumber (cm⁻¹)',
        yLabel: 'Transmittance (%)',
        peaks: [
          { x: 3036, y: 78, label: 'C-H stretch (arom)' },
          { x: 1480, y: 55, label: 'C=C ring stretch' },
          { x: 1035, y: 60, label: 'C-H in-plane bend' },
          { x: 674, y: 40, label: 'C-H out-of-plane bend' }
        ],
        dataPoints: [
          [400, 92], [500, 82], [674, 40], [800, 65], [900, 72],
          [1000, 62], [1035, 60], [1100, 68], [1200, 75], [1300, 70],
          [1400, 60], [1480, 55], [1600, 70], [1800, 82], [2000, 85],
          [2200, 88], [2400, 90], [2600, 85], [2800, 80], [3000, 78],
          [3036, 78], [3200, 72], [3400, 65], [3600, 50], [4000, 42]
        ]
      },
      {
        id: 'spec-4-uv',
        type: 'UV-Vis',
        name: 'Benzene UV-Vis Spectrum',
        instrument: 'Shimadzu UV-2600',
        conditions: 'Cyclohexane, 200-400 nm, RT',
        xLabel: 'Wavelength (nm)',
        yLabel: 'Absorbance',
        peaks: [
          { x: 255, y: 0.82, label: 'π→π* (¹B₂ᵤ)' },
          { x: 204, y: 0.95, label: 'π→π* (¹B₁ᵤ)' }
        ],
        dataPoints: [
          [190, 0.30], [200, 0.85], [204, 0.95], [210, 0.60], [220, 0.35],
          [230, 0.20], [240, 0.32], [248, 0.60], [252, 0.78], [255, 0.82],
          [258, 0.70], [262, 0.45], [270, 0.18], [280, 0.08], [290, 0.05],
          [300, 0.02], [320, 0.01], [350, 0], [380, 0], [400, 0]
        ]
      }
    ]
  },
  {
    picId: 6,
    spectra: [
      {
        id: 'spec-6-ir',
        type: 'IR',
        name: 'Ammonia FTIR Spectrum',
        instrument: 'Bruker VERTEX 70',
        conditions: 'Gas cell, 400-4000 cm⁻¹, RT',
        xLabel: 'Wavenumber (cm⁻¹)',
        yLabel: 'Transmittance (%)',
        peaks: [
          { x: 3336, y: 70, label: 'N-H stretch (asym)' },
          { x: 1628, y: 55, label: 'H-N-H bend (asym)' },
          { x: 950, y: 48, label: 'N-H bend (sym)' }
        ],
        dataPoints: [
          [400, 90], [600, 82], [800, 55], [950, 48], [1100, 60],
          [1300, 68], [1500, 52], [1628, 55], [1800, 72], [2000, 80],
          [2200, 85], [2400, 88], [2600, 84], [2800, 78], [3000, 72],
          [3200, 65], [3336, 70], [3500, 55], [3700, 40], [4000, 35]
        ]
      },
      {
        id: 'spec-6-raman',
        type: 'Raman',
        name: 'Ammonia Raman Spectrum',
        instrument: 'Horiba LabRAM HR',
        conditions: '532 nm laser, 100-4000 cm⁻¹, RT',
        xLabel: 'Raman Shift (cm⁻¹)',
        yLabel: 'Intensity (a.u.)',
        peaks: [
          { x: 3334, y: 88, label: 'N-H stretch' },
          { x: 950, y: 62, label: 'Symmetric deformation' }
        ],
        dataPoints: [
          [100, 5], [300, 8], [500, 10], [700, 18], [900, 55],
          [950, 62], [1000, 35], [1200, 12], [1500, 10], [1800, 8],
          [2000, 15], [2400, 10], [2800, 20], [3000, 35], [3200, 70],
          [3334, 88], [3500, 40], [3700, 15], [4000, 8]
        ]
      }
    ]
  }
]

// =============== Mock Category Summary ===============
export const mockCategorySummary = [
  { category: '无机小分子', count: 2341, percentage: 18.8 },
  { category: '有机小分子', count: 4521, percentage: 36.3 },
  { category: '芳香族化合物', count: 1876, percentage: 15.1 },
  { category: '无机盐', count: 1203, percentage: 9.7 },
  { category: '烯烃', count: 892, percentage: 7.2 },
  { category: '无机酸', count: 523, percentage: 4.2 },
  { category: '过渡金属配合物', count: 678, percentage: 5.4 },
  { category: '其他', count: 422, percentage: 3.4 }
]

// =============== Mock Molecule Summary Documents ===============
export const mockMoleculeSummary = [
  { id: 1, title: '小分子化合物数据库概述', description: '涵盖常见无机和有机小分子的结构、性质和谱学数据，包含IR、NMR、MS等多维表征信息。', category: 'organic', updateTime: '2026-06-10' },
  { id: 2, title: '过渡金属催化剂数据集', description: '包含Fe、Co、Ni、Cu、Pd、Pt等多种过渡金属的催化体系数据，涵盖均相和异相催化反应。', category: 'catalyst', updateTime: '2026-05-28' },
  { id: 3, title: '芳香族化合物光谱合集', description: '收录苯系、萘系、杂环芳香族化合物的IR、NMR、MS、UV-Vis谱图数据。', category: 'spectra', updateTime: '2026-06-01' },
  { id: 4, title: '计算化学基准数据集', description: '基于DFT计算的分子结构优化、频率分析和热力学数据，包含多种泛函和基组水平计算结果。', category: 'computational', updateTime: '2026-05-15' },
  { id: 5, title: '谱学标准参考数据集', description: '收录常见官能团和化合物的标准谱图数据，用于谱图解析和结构鉴定参考。', category: 'spectra', updateTime: '2026-04-20' }
]

// =============== Mock Object Storage Files ===============
export const mockObsFiles = [
  { id: 'obs-001', name: 'h2o_spectrum_raw.fid', size: 2457600, type: 'application/octet-stream', uploadTime: '2026-06-01 10:30:00', moleculeId: 1, description: 'H₂O NMR raw FID data (Bruker format)' },
  { id: 'obs-002', name: 'benzene_ftir.dpt', size: 102400, type: 'application/octet-stream', uploadTime: '2026-05-15 14:20:00', moleculeId: 4, description: 'Benzene FTIR data file (Thermo format)' },
  { id: 'obs-003', name: 'ethanol_ms_spectrum.mzML', size: 5120000, type: 'application/xml', uploadTime: '2026-05-20 09:15:00', moleculeId: 3, description: 'Ethanol GC-MS spectrum in mzML format' },
  { id: 'obs-004', name: 'ammonia_raman.spc', size: 81920, type: 'application/octet-stream', uploadTime: '2026-04-05 16:45:00', moleculeId: 6, description: 'Ammonia Raman spectrum (GRAMS SPC format)' },
  { id: 'obs-005', name: 'water_optimization.chk', size: 8388608, type: 'application/octet-stream', uploadTime: '2026-06-08 11:00:00', moleculeId: 1, description: 'H₂O DFT optimization checkpoint file (Gaussian)' },
  { id: 'obs-006', name: 'benzene_crystal.cif', size: 5120, type: 'chemical/x-cif', uploadTime: '2026-05-30 08:30:00', moleculeId: 4, description: 'Benzene crystal structure CIF file' }
]

// =============== Mock Spectrum Types for Search ===============
export const mockSpectrumTypes = [
  { type: 'IR', label: '红外光谱 (IR)', count: 4520 },
  { type: 'NMR', label: '核磁共振 (NMR)', count: 3800 },
  { type: 'MS', label: '质谱 (MS)', count: 5100 },
  { type: 'Raman', label: '拉曼光谱 (Raman)', count: 1200 },
  { type: 'UV-Vis', label: '紫外-可见 (UV-Vis)', count: 2300 },
  { type: 'XRD', label: 'X射线衍射 (XRD)', count: 890 }
]

// =============== Mock AI Knowledge Base ===============
const MOLECULE_DB = {
  'h2o': { formula: 'H₂O', name: '水', mass: '18.015 g/mol', type: '无机小分子', smiles: 'O', desc: '水是最常见的无机小分子，由两个氢原子和一个氧原子组成。广泛用作溶剂，在化学反应中扮演重要角色。其IR谱在3450 cm⁻¹处有O-H伸缩振动峰，1640 cm⁻¹处有弯曲振动峰。' },
  'ch4': { formula: 'CH₄', name: '甲烷', mass: '16.043 g/mol', type: '有机小分子', smiles: 'C', desc: '甲烷是最简单的烷烃，由一个碳原子和四个氢原子组成。是天然气的主要成分，也是一种重要的温室气体。' },
  'c2h5oh': { formula: 'C₂H₅OH', name: '乙醇', mass: '46.069 g/mol', type: '有机小分子', smiles: 'CCO', desc: '乙醇是常见的醇类化合物，俗称酒精。广泛用作溶剂、消毒剂和燃料添加剂。其IR谱在3340 cm⁻¹处有O-H伸缩振动峰。可通过质谱（MS）和NMR进行结构表征。' },
  'c6h6': { formula: 'C₆H₆', name: '苯', mass: '78.114 g/mol', type: '芳香族化合物', smiles: 'c1ccccc1', desc: '苯是最简单的芳香族化合物，具有六元环结构。是重要的有机化工原料和溶剂。其UV-Vis谱在255 nm处有特征吸收峰（π→π*跃迁），IR谱在3036 cm⁻¹处有芳香C-H伸缩振动。' },
  'co2': { formula: 'CO₂', name: '二氧化碳', mass: '44.009 g/mol', type: '无机小分子', smiles: 'O=C=O', desc: '二氧化碳是一种线性三原子分子，是光合作用的碳源。也是主要的温室气体之一。其IR谱在2349 cm⁻¹处有不对称伸缩振动特征峰。' },
  'nh3': { formula: 'NH₃', name: '氨', mass: '17.031 g/mol', type: '无机小分子', smiles: 'N', desc: '氨是一种三角锥形的含氮小分子，具有碱性。广泛用于化肥生产和化工合成。其Raman谱在3334 cm⁻¹处有N-H伸缩振动峰。' },
  'ch3cooh': { formula: 'CH₃COOH', name: '乙酸', mass: '60.052 g/mol', type: '有机小分子', smiles: 'CC(=O)O', desc: '乙酸是最简单的羧酸，俗称醋酸。具有羧基（-COOH）官能团，可与碱发生中和反应。' },
  'nacl': { formula: 'NaCl', name: '氯化钠', mass: '58.44 g/mol', type: '无机盐', smiles: '[Na+].[Cl-]', desc: '氯化钠是典型的离子化合物，俗称食盐。具有面心立方晶体结构，在水中完全电离为Na⁺和Cl⁻。' },
  'c2h4': { formula: 'C₂H₄', name: '乙烯', mass: '28.054 g/mol', type: '烯烃', smiles: 'C=C', desc: '乙烯是最简单的烯烃，含有碳碳双键。是重要的石化基础原料，用于合成聚乙烯等聚合物。其C=C双键特征IR吸收在1640-1680 cm⁻¹。' },
  'h2so4': { formula: 'H₂SO₄', name: '硫酸', mass: '98.079 g/mol', type: '无机酸', smiles: 'OS(=O)(=O)O', desc: '硫酸是一种强二元无机酸，具有强氧化性和脱水性。是化工行业最重要的基础原料之一。' }
}

// AI response templates for different query categories
export function generateAiResponse(message, moleculeList) {
  const msg = message.toLowerCase().trim()

  // 1. Element query
  const elementMap = {
    'h': '元素 H（氢）：原子序数 1，原子质量 1.008 u，位于元素周期表第1周期IA族。氢是宇宙中丰度最高的元素，可形成 H₂O、NH₃、CH₄ 等多种化合物。平台收录含氢分子超过8000条。',
    'c': '元素 C（碳）：原子序数 6，原子质量 12.011 u，位于元素周期表第2周期IVA族。碳是有机化学的基础，可形成 sp/sp²/sp³ 多种杂化。平台收录有机分子数据超过4500条。',
    'o': '元素 O（氧）：原子序数 8，原子质量 15.999 u，位于元素周期表第2周期VIA族。氧是地壳中含量最高的元素，广泛存在于水和有机物中。',
    'n': '元素 N（氮）：原子序数 7，原子质量 14.007 u，位于元素周期表第2周期VA族。氮是氨基酸和蛋白质的重要组成部分，大气中含量最高的元素。',
    'fe': '元素 Fe（铁）：原子序数 26，原子质量 55.845 u，位于第4周期VIII族。铁是重要的过渡金属，在催化、磁性材料等领域有广泛应用。平台收录含铁催化剂数据超过600条。',
    'cu': '元素 Cu（铜）：原子序数 29，原子质量 63.546 u，位于第4周期IB族。铜在催化、导电材料领域应用广泛，Cu(111)表面是重要的催化模型体系。',
    'pt': '元素 Pt（铂）：原子序数 78，原子质量 195.084 u，位于第6周期VIII族。铂是重要的贵金属催化剂，Pt(111)表面在电催化中有广泛应用。',
    'na': '元素 Na（钠）：原子序数 11，原子质量 22.990 u，位于第3周期IA族。钠是活泼的碱金属，常以离子形式存在于化合物中，如 NaCl、NaOH。',
    'cl': '元素 Cl（氯）：原子序数 17，原子质量 35.45 u，位于第3周期VIIA族。氯是活泼的非金属卤族元素，常以 Cl⁻ 离子形式存在。'
  }
  for (const [elem, reply] of Object.entries(elementMap)) {
    if (msg === elem || msg.includes('元素 ' + elem) || msg.includes('元素' + elem) || msg.includes(elem + '元素') || msg.includes(elem + ' 原子') || msg.match(new RegExp('查询.*' + elem, 'i'))) {
      return { reply, actions: [{ text: '查看元素周期表', icon: 'el-icon-s-grid', path: '/molecule' }] }
    }
  }

  // 2. Formula query
  for (const [key, mol] of Object.entries(MOLECULE_DB)) {
    if (msg.includes(key) || msg.includes(mol.formula.toLowerCase()) || msg.includes(mol.name)) {
      const idMap = { 'h2o': 1, 'ch4': 2, 'c2h5oh': 3, 'c6h6': 4, 'co2': 5, 'nh3': 6, 'ch3cooh': 7, 'nacl': 9, 'c2h4': 10, 'h2so4': 11 }
      const id = idMap[key]
      return {
        reply: `${mol.formula}（${mol.name}）\n\n类型：${mol.type} | 分子质量：${mol.mass} | SMILES：${mol.smiles}\n\n${mol.desc}`,
        actions: id ? [
          { text: '查看分子详情', icon: 'el-icon-view', path: '/molecule-detail/' + id },
          { text: '查看谱学数据', icon: 'el-icon-data-line', path: '/molecule-detail/' + id + '?tab=spectrum' }
        ] : []
      }
    }
  }

  // 3. Spectrum query
  if (msg.includes('谱') || msg.includes('光谱') || msg.includes('ir') || msg.includes('nmr') || msg.includes('质谱') || msg.includes('拉曼') || msg.includes('紫外')) {
    let spectraReply = '平台提供以下谱学数据：\n\n'
    spectraReply += '• IR 红外光谱（4,520条）：分子振动信息，可识别官能团\n'
    spectraReply += '• NMR 核磁共振谱（3,800条）：化学位移信息，可确定分子结构\n'
    spectraReply += '• MS 质谱（5,100条）：质荷比信息，可确定分子量和碎片结构\n'
    spectraReply += '• Raman 拉曼光谱（1,200条）：互补于IR的分子振动信息\n'
    spectraReply += '• UV-Vis 紫外-可见光谱（2,300条）：电子跃迁信息\n'
    spectraReply += '\n在分子详情页点击"谱学数据"Tab即可查看对应图谱。'
    return {
      reply: spectraReply,
      actions: [
        { text: '谱学类型搜索', icon: 'el-icon-search', path: '/molecule' },
        { text: '查看示例（H₂O）', icon: 'el-icon-view', path: '/molecule-detail/1' }
      ]
    }
  }

  // 4. Upload query
  if (msg.includes('上传') || msg.includes('提交') || msg.includes('导入') || msg.includes('数据格式') || msg.includes('模板')) {
    return {
      reply: '平台支持通用分子文件上传，格式包括：.json、.csv、.xyz、.cif、POSCAR、OUTCAR 等。\n\n上传流程：\n1. 选择上传模板（分子结构/材料性质/催化数据）\n2. 上传文件并选择处理工具（VASP/ASE/LAMMPS/Gaussian）\n3. 填写元数据（计算方法、基组、温度、压力等）\n4. 确认提交\n\n上传接口：POST /api/v1/molecule/open/upload',
      actions: [{ text: '前往上传页面', icon: 'el-icon-upload2', path: '/upload_data' }]
    }
  }

  // 5. Search / API query
  if (msg.includes('搜索') || msg.includes('查找') || msg.includes('检索') || msg.includes('查询') || msg.includes('api')) {
    return {
      reply: '您可以通过以下方式检索分子数据：\n\n1. 关键词搜索：输入分子式、SMILES或标签\n2. 高级搜索：按分子式、质量范围、电荷、自旋、分类筛选\n3. 谱学类型搜索：按IR/NMR/MS/Raman/UV-Vis/ XRD筛选\n4. API接口：POST /api/v1/molecule/open/search/core\n\n建议在分子列表页使用高级搜索功能获得更精准的结果。',
      actions: [
        { text: '分子高级搜索', icon: 'el-icon-search', path: '/molecule' },
        { text: '查看API文档', icon: 'el-icon-document', path: '/api-info' }
      ]
    }
  }

  // 6. Material query
  if (msg.includes('材料') || msg.includes('催化') || msg.includes('表面') || msg.includes('晶体') || msg.includes('二维材料')) {
    return {
      reply: '平台收录了丰富的材料数据，包括：\n\n• 金属表面（如Cu(111)、Pt(111)）\n• 金属氧化物（如TiO₂、ZnO、Fe₂O₃）\n• 二维材料（如石墨烯、MoS₂）\n• 催化材料体系\n\n每条数据包含：能带间隙、晶格常数、晶体结构、空间群等信息。支持按类型和标签筛选。',
      actions: [
        { text: '查看材料列表', icon: 'el-icon-s-grid', path: '/materials' },
        { text: '查看催化详情', icon: 'el-icon-data-line', path: '/catalytic-detail/1' }
      ]
    }
  }

  // 7. Similarity / structure query
  if (msg.includes('相似') || msg.includes('结构') || msg.includes('smiles') || msg.includes('2d') || msg.includes('3d')) {
    return {
      reply: '平台提供2D和3D分子相似性搜索功能：\n\n• 2D相似性：基于分子指纹（Morgan/ECFP4）的Tanimoto相似度\n• 3D相似性：基于三维构象的形状和静电势相似度\n• 输入SMILES表达式并设置阈值即可搜索结构相似的分子\n\n例如输入 c1ccccc1（苯的SMILES）可搜索芳香族类似物。',
      actions: [{ text: '相似性搜索', icon: 'el-icon-connection', path: '/molecule-similarity' }]
    }
  }

  // 8. Data / statistics query
  if (msg.includes('统计') || msg.includes('数量') || msg.includes('多少') || msg.includes('数据量') || msg.includes('概况')) {
    const total = (moleculeList || []).reduce((s, c) => s + c.count, 12456)
    return {
      reply: `平台数据概况：\n\n• 分子数据总量：${total.toLocaleString()} 条\n• 材料数据总量：5,832 条\n• 文献数据总量：3,201 条\n• 谱学数据总量：17,810 条\n\n分子按分类：有机小分子(36.3%) > 无机小分子(18.8%) > 芳香族化合物(15.1%) > 无机盐(9.7%) > 烯烃(7.2%) > 过渡金属配合物(5.4%) > 无机酸(4.2%) > 其他(3.4%)`,
      actions: [{ text: '返回首页看板', icon: 'el-icon-s-home', path: '/home' }]
    }
  }

  // 9. Help / general query
  if (msg.includes('帮助') || msg.includes('功能') || msg.includes('怎么用') || msg.includes('能做什么') || msg.includes('介绍')) {
    return {
      reply: '精准化学数据平台（PIChemData）提供以下功能：\n\n🔍 分子数据检索——按关键词、分类、分子式、谱学类型等多维度搜索\n📊 材料数据查询——金属/氧化物/二维材料的结构与性质数据\n📄 文献数据检索——催化、材料领域高水平论文数据\n📈 谱学数据浏览——IR、NMR、MS、Raman、UV-Vis、XRD图谱\n🤖 智能助手——自然语言交互式数据查询\n🔗 API接口——RESTful API支持程序化数据访问\n📤 数据上传——标准模板化的数据提交与审核\n\n请直接输入您感兴趣的内容，如分子式、元素名或功能需求。',
      actions: []
    }
  }

  // 10. Default / fallback
  return {
    reply: '根据您的提问，我建议：\n\n1. 如果查询特定化合物，请直接输入分子式（如 H2O、C6H6）或名称（如 水、苯）\n2. 如果查询元素信息，请输入元素符号（如 H、Fe、Cu）\n3. 如需谱学数据，请输入"光谱"或具体谱学类型（如 IR）\n4. 如需上传数据，请输入"上传"\n5. 输入"帮助"查看平台完整功能\n\n您也可以访问以下页面获取信息：',
    actions: [
      { text: '分子列表', icon: 'el-icon-search', path: '/molecule' },
      { text: '首页看板', icon: 'el-icon-s-home', path: '/home' }
    ]
  }
}
