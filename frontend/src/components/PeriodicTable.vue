<template>
  <div class="periodic-table">
    <div class="pt-header">
      <h4>元素周期表 - 选择元素</h4>
      <div class="selected-elements">
        <el-tag
          v-for="el in selectedElements"
          :key="el"
          closable
          @close="removeElement(el)"
          size="small"
          style="margin-right:4px;margin-bottom:4px"
        >{{ el }}</el-tag>
        <span v-if="!selectedElements.length" style="color:#999;font-size:12px">点击元素进行选择</span>
      </div>
      <el-button size="mini" @click="clearAll">清空</el-button>
    </div>
    <div class="pt-grid">
      <div
        v-for="el in elements"
        :key="el.symbol"
        :class="['pt-element', 'cat-' + el.category, { selected: selectedElements.includes(el.symbol) }]"
        :style="{ gridRow: el.row, gridColumn: el.col }"
        @click="toggleElement(el.symbol)"
        :title="el.name + ' (' + el.symbol + ') - ' + el.atomicMass"
      >
        <span class="pt-number">{{ el.number }}</span>
        <span class="pt-symbol">{{ el.symbol }}</span>
        <span class="pt-name">{{ el.name }}</span>
      </div>
    </div>
    <!-- Legend -->
    <div class="pt-legend">
      <span class="legend-item"><span class="dot cat-alkali"></span> 碱金属</span>
      <span class="legend-item"><span class="dot cat-alkaline"></span> 碱土金属</span>
      <span class="legend-item"><span class="dot cat-transition"></span> 过渡金属</span>
      <span class="legend-item"><span class="dot cat-post-transition"></span> 后过渡金属</span>
      <span class="legend-item"><span class="dot cat-metalloid"></span> 类金属</span>
      <span class="legend-item"><span class="dot cat-nonmetal"></span> 非金属</span>
      <span class="legend-item"><span class="dot cat-halogen"></span> 卤素</span>
      <span class="legend-item"><span class="dot cat-noble-gas"></span> 稀有气体</span>
    </div>
  </div>
</template>

<script>
const ELEMENTS = [
  // Row 1
  { symbol: 'H', name: '氢', number: 1, category: 'nonmetal', row: 1, col: 1, atomicMass: 1.008 },
  { symbol: 'He', name: '氦', number: 2, category: 'noble-gas', row: 1, col: 18, atomicMass: 4.003 },
  // Row 2
  { symbol: 'Li', name: '锂', number: 3, category: 'alkali', row: 2, col: 1, atomicMass: 6.941 },
  { symbol: 'Be', name: '铍', number: 4, category: 'alkaline', row: 2, col: 2, atomicMass: 9.012 },
  { symbol: 'B', name: '硼', number: 5, category: 'metalloid', row: 2, col: 13, atomicMass: 10.811 },
  { symbol: 'C', name: '碳', number: 6, category: 'nonmetal', row: 2, col: 14, atomicMass: 12.011 },
  { symbol: 'N', name: '氮', number: 7, category: 'nonmetal', row: 2, col: 15, atomicMass: 14.007 },
  { symbol: 'O', name: '氧', number: 8, category: 'nonmetal', row: 2, col: 16, atomicMass: 15.999 },
  { symbol: 'F', name: '氟', number: 9, category: 'halogen', row: 2, col: 17, atomicMass: 18.998 },
  { symbol: 'Ne', name: '氖', number: 10, category: 'noble-gas', row: 2, col: 18, atomicMass: 20.180 },
  // Row 3
  { symbol: 'Na', name: '钠', number: 11, category: 'alkali', row: 3, col: 1, atomicMass: 22.990 },
  { symbol: 'Mg', name: '镁', number: 12, category: 'alkaline', row: 3, col: 2, atomicMass: 24.305 },
  { symbol: 'Al', name: '铝', number: 13, category: 'post-transition', row: 3, col: 13, atomicMass: 26.982 },
  { symbol: 'Si', name: '硅', number: 14, category: 'metalloid', row: 3, col: 14, atomicMass: 28.086 },
  { symbol: 'P', name: '磷', number: 15, category: 'nonmetal', row: 3, col: 15, atomicMass: 30.974 },
  { symbol: 'S', name: '硫', number: 16, category: 'nonmetal', row: 3, col: 16, atomicMass: 32.065 },
  { symbol: 'Cl', name: '氯', number: 17, category: 'halogen', row: 3, col: 17, atomicMass: 35.453 },
  { symbol: 'Ar', name: '氩', number: 18, category: 'noble-gas', row: 3, col: 18, atomicMass: 39.948 },
  // Row 4
  { symbol: 'K', name: '钾', number: 19, category: 'alkali', row: 4, col: 1, atomicMass: 39.098 },
  { symbol: 'Ca', name: '钙', number: 20, category: 'alkaline', row: 4, col: 2, atomicMass: 40.078 },
  { symbol: 'Sc', name: '钪', number: 21, category: 'transition', row: 4, col: 3, atomicMass: 44.956 },
  { symbol: 'Ti', name: '钛', number: 22, category: 'transition', row: 4, col: 4, atomicMass: 47.867 },
  { symbol: 'V', name: '钒', number: 23, category: 'transition', row: 4, col: 5, atomicMass: 50.942 },
  { symbol: 'Cr', name: '铬', number: 24, category: 'transition', row: 4, col: 6, atomicMass: 51.996 },
  { symbol: 'Mn', name: '锰', number: 25, category: 'transition', row: 4, col: 7, atomicMass: 54.938 },
  { symbol: 'Fe', name: '铁', number: 26, category: 'transition', row: 4, col: 8, atomicMass: 55.845 },
  { symbol: 'Co', name: '钴', number: 27, category: 'transition', row: 4, col: 9, atomicMass: 58.933 },
  { symbol: 'Ni', name: '镍', number: 28, category: 'transition', row: 4, col: 10, atomicMass: 58.693 },
  { symbol: 'Cu', name: '铜', number: 29, category: 'transition', row: 4, col: 11, atomicMass: 63.546 },
  { symbol: 'Zn', name: '锌', number: 30, category: 'transition', row: 4, col: 12, atomicMass: 65.390 },
  { symbol: 'Ga', name: '镓', number: 31, category: 'post-transition', row: 4, col: 13, atomicMass: 69.723 },
  { symbol: 'Ge', name: '锗', number: 32, category: 'metalloid', row: 4, col: 14, atomicMass: 72.640 },
  { symbol: 'As', name: '砷', number: 33, category: 'metalloid', row: 4, col: 15, atomicMass: 74.922 },
  { symbol: 'Se', name: '硒', number: 34, category: 'nonmetal', row: 4, col: 16, atomicMass: 78.960 },
  { symbol: 'Br', name: '溴', number: 35, category: 'halogen', row: 4, col: 17, atomicMass: 79.904 },
  { symbol: 'Kr', name: '氪', number: 36, category: 'noble-gas', row: 4, col: 18, atomicMass: 83.800 },
  // Row 5
  { symbol: 'Rb', name: '铷', number: 37, category: 'alkali', row: 5, col: 1, atomicMass: 85.468 },
  { symbol: 'Sr', name: '锶', number: 38, category: 'alkaline', row: 5, col: 2, atomicMass: 87.620 },
  { symbol: 'Y', name: '钇', number: 39, category: 'transition', row: 5, col: 3, atomicMass: 88.906 },
  { symbol: 'Zr', name: '锆', number: 40, category: 'transition', row: 5, col: 4, atomicMass: 91.224 },
  { symbol: 'Nb', name: '铌', number: 41, category: 'transition', row: 5, col: 5, atomicMass: 92.906 },
  { symbol: 'Mo', name: '钼', number: 42, category: 'transition', row: 5, col: 6, atomicMass: 95.940 },
  { symbol: 'Tc', name: '锝', number: 43, category: 'transition', row: 5, col: 7, atomicMass: 98.000 },
  { symbol: 'Ru', name: '钌', number: 44, category: 'transition', row: 5, col: 8, atomicMass: 101.070 },
  { symbol: 'Rh', name: '铑', number: 45, category: 'transition', row: 5, col: 9, atomicMass: 102.906 },
  { symbol: 'Pd', name: '钯', number: 46, category: 'transition', row: 5, col: 10, atomicMass: 106.420 },
  { symbol: 'Ag', name: '银', number: 47, category: 'transition', row: 5, col: 11, atomicMass: 107.868 },
  { symbol: 'Cd', name: '镉', number: 48, category: 'transition', row: 5, col: 12, atomicMass: 112.411 },
  { symbol: 'In', name: '铟', number: 49, category: 'post-transition', row: 5, col: 13, atomicMass: 114.818 },
  { symbol: 'Sn', name: '锡', number: 50, category: 'post-transition', row: 5, col: 14, atomicMass: 118.710 },
  { symbol: 'Sb', name: '锑', number: 51, category: 'metalloid', row: 5, col: 15, atomicMass: 121.760 },
  { symbol: 'Te', name: '碲', number: 52, category: 'metalloid', row: 5, col: 16, atomicMass: 127.600 },
  { symbol: 'I', name: '碘', number: 53, category: 'halogen', row: 5, col: 17, atomicMass: 126.904 },
  { symbol: 'Xe', name: '氙', number: 54, category: 'noble-gas', row: 5, col: 18, atomicMass: 131.293 },
  // Row 6
  { symbol: 'Cs', name: '铯', number: 55, category: 'alkali', row: 6, col: 1, atomicMass: 132.905 },
  { symbol: 'Ba', name: '钡', number: 56, category: 'alkaline', row: 6, col: 2, atomicMass: 137.327 },
  { symbol: 'Hf', name: '铪', number: 72, category: 'transition', row: 6, col: 4, atomicMass: 178.490 },
  { symbol: 'Ta', name: '钽', number: 73, category: 'transition', row: 6, col: 5, atomicMass: 180.948 },
  { symbol: 'W', name: '钨', number: 74, category: 'transition', row: 6, col: 6, atomicMass: 183.840 },
  { symbol: 'Re', name: '铼', number: 75, category: 'transition', row: 6, col: 7, atomicMass: 186.207 },
  { symbol: 'Os', name: '锇', number: 76, category: 'transition', row: 6, col: 8, atomicMass: 190.230 },
  { symbol: 'Ir', name: '铱', number: 77, category: 'transition', row: 6, col: 9, atomicMass: 192.217 },
  { symbol: 'Pt', name: '铂', number: 78, category: 'transition', row: 6, col: 10, atomicMass: 195.078 },
  { symbol: 'Au', name: '金', number: 79, category: 'transition', row: 6, col: 11, atomicMass: 196.967 },
  { symbol: 'Hg', name: '汞', number: 80, category: 'transition', row: 6, col: 12, atomicMass: 200.590 },
  { symbol: 'Pb', name: '铅', number: 82, category: 'post-transition', row: 6, col: 14, atomicMass: 207.200 },
  { symbol: 'Bi', name: '铋', number: 83, category: 'post-transition', row: 6, col: 15, atomicMass: 208.980 },
]

export default {
  name: 'PeriodicTable',
  props: {
    value: { type: Array, default: () => [] }
  },
  data() {
    return { elements: ELEMENTS }
  },
  computed: {
    selectedElements: {
      get() { return this.value },
      set(v) { this.$emit('input', v) }
    }
  },
  methods: {
    toggleElement(symbol) {
      const idx = this.selectedElements.indexOf(symbol)
      if (idx >= 0) {
        this.selectedElements = this.selectedElements.filter(s => s !== symbol)
      } else {
        this.selectedElements = [...this.selectedElements, symbol]
      }
    },
    removeElement(symbol) {
      this.selectedElements = this.selectedElements.filter(s => s !== symbol)
    },
    clearAll() {
      this.selectedElements = []
    }
  }
}
</script>

<style scoped>
.periodic-table {
  padding: 16px;
}
.pt-header {
  margin-bottom: 16px;
}
.pt-header h4 {
  margin: 0 0 8px;
  color: #1a4a80;
}
.selected-elements {
  margin: 8px 0;
  min-height: 24px;
}
.pt-grid {
  display: grid;
  grid-template-columns: repeat(18, 50px);
  grid-template-rows: repeat(7, 60px);
  gap: 2px;
  justify-content: center;
}
.pt-element {
  border: 1px solid #ddd;
  border-radius: 3px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 10px;
  position: relative;
}
.pt-element:hover {
  transform: scale(1.15);
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.pt-element.selected {
  border: 2px solid #1a4a80;
  background: #e6f0fa !important;
  transform: scale(1.1);
  z-index: 5;
}
.pt-number {
  position: absolute;
  top: 1px;
  left: 3px;
  font-size: 8px;
  color: #666;
}
.pt-symbol {
  font-size: 15px;
  font-weight: bold;
  margin-top: 4px;
}
.pt-name {
  font-size: 8px;
  color: #666;
}
/* Category colors */
.cat-alkali { background: #ffcdd2; }
.cat-alkaline { background: #ffe0b2; }
.cat-transition { background: #fff9c4; }
.cat-post-transition { background: #c8e6c9; }
.cat-metalloid { background: #b2dfdb; }
.cat-nonmetal { background: #e1f5fe; }
.cat-halogen { background: #f3e5f5; }
.cat-noble-gas { background: #ffccbc; }
/* Legend */
.pt-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
  font-size: 12px;
  justify-content: center;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.dot {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  border: 1px solid #ddd;
}
</style>
