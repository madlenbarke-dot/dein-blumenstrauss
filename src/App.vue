<template>
  <div class="container" :class="{ 'party-mode': partyMode, falling, rising }" :style="containerStyle">
    <div 
      class="cell" 
      v-for="(flower, index) in flowers" 
      :key="index" 
      :class="{ rotated: rotatedCells.has(index), special: index === specialCell, party: index === partyCell }" 
      :style="{ 
        left: `${flower.x}px`, 
        top: `${flower.y}px`,
        width: `${flowerSize}px`,
        height: `${flowerSize}px`,
        animationDelay: (falling || rising) ? `${Math.random() * 0.8}s` : undefined
      }" 
      @click="onCellClick(index)"
    >
      <img :src="flower.image" alt="flower" />
    </div>
  </div>

  <dialog ref="dialogRef" class="flower-dialog" @cancel.prevent>
    <button class="close-button" @click="closeDialog">&times;</button>

    <template v-if="dialogStep === 'ask'">
      <div style="color: white">Verbringst du den Valentinstag mit mir?</div>
      <div class="dialog-buttons">
        <button class="fall-button" @click="answerYes">Ja</button>
        <button class="fall-button" @click="answerNo">Nein</button>
      </div>
    </template>

    <template v-if="dialogStep === 'sure'">
      <div style="color: white">Bist du sicher?</div>
      <div class="dialog-buttons">
        <button ref="runawayRef" class="fall-button runaway" :style="{ transform: `translate(${runawayOffset.x}px, ${runawayOffset.y}px)` }" @mouseover="moveRunaway" @touchstart.prevent="moveRunaway" @click="sureYes">Ja</button>
        <button class="fall-button" @click="sureNo">Nein</button>
      </div>
    </template>

    <template v-if="dialogStep === 'party'">
      <div style="color: white">yeeeeeeeeaaaah!</div>
    </template>
  </dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

import flower1 from '@/assets/images/flower_1.png'
import flower2 from '@/assets/images/flower_2.png'
import flower3 from '@/assets/images/flower_3.png'
import flower4 from '@/assets/images/flower_4.png'
import flower5 from '@/assets/images/flower_5.png'
import flower6 from '@/assets/images/flower_6.png'
import meadowBg from '@/assets/images/meadow-background.jpg'
import partyMusic from '@/assets/music/partyonwebbi.wav'

const images = [flower1, flower2, flower3, flower4, flower5, flower6]
const audio = new Audio(partyMusic)
audio.addEventListener('timeupdate', () => {
  if (audio.duration - audio.currentTime <= 0.3) {
    audio.currentTime = 0.95
  }
})

const width = ref(window.innerWidth)
const height = ref(window.innerHeight)



const isMobile = computed(() => width.value < 768)
const targetSize = computed(() => isMobile.value ? 150 : 250)
const minSize = computed(() => isMobile.value ? 120 : 200)
const maxSize = computed(() => isMobile.value ? 180 : 300)
const gap = 30

const rotatedCells = ref(new Set<number>())
const partyMode = ref(false)
const falling = ref(false)

const dialogRef = ref<HTMLDialogElement>()

function toggleRotation(i: number) {
  if (rotatedCells.value.has(i)) {
    rotatedCells.value.delete(i)
  } else {
    rotatedCells.value.add(i)
  }
  rotatedCells.value = new Set(rotatedCells.value)
}

function onCellClick(i: number) {
  if (i === specialCell.value) {
    dialogStep.value = 'ask'
    dialogRef.value?.showModal()
  } else if (i === partyCell.value) {
    partyMode.value = !partyMode.value
    if (partyMode.value) {
      audio.currentTime = 0.95
      audio.play()
    } else {
      audio.pause()
    }
  } else {
    toggleRotation(i)
  }
}

const dialogStep = ref<'ask' | 'sure' | 'party'>('ask')

function closeDialog() {
  dialogRef.value?.close()
  dialogStep.value = 'ask'
  if (partyMode.value) {
    stopParty()
  }
}

const rising = ref(false)

function startParty() {
  partyMode.value = true
  audio.currentTime = 0.95
  audio.play()
}

function stopParty() {
  partyMode.value = false
  audio.pause()
}

function dropFlowers() {
  rising.value = false
  falling.value = true
}

function riseFlowers() {
  falling.value = false
  rising.value = true
}

function answerYes() {
  dialogStep.value = 'party'
  startParty()
}

function answerNo() {
  dialogStep.value = 'sure'
  dropFlowers()
}

function flowerExplosion() {
  const duration = 5000 // Explosion lasts 5 seconds
  const interval = 50 // New flower every 50ms
  const endTime = Date.now() + duration
  
  const explosionInterval = setInterval(() => {
    if (Date.now() > endTime) {
      clearInterval(explosionInterval)
      return
    }
    
    // Add multiple flowers at once for explosion effect
    for (let i = 0; i < 5; i++) {
        // Start at center
        const startX = width.value / 2 - flowerSize.value / 2
        const startY = height.value / 2 - flowerSize.value / 2
        
        // Target random position
        const targetX = Math.random() * (width.value - flowerSize.value)
        const targetY = Math.random() * (height.value - flowerSize.value)
        
        const newFlower = {
            x: startX,
            y: startY,
            image: images[Math.floor(Math.random() * images.length)] as string,
            index: flowers.value.length
        }
        
        flowers.value.push(newFlower)
        
        // Animate to target position in next tick
        setTimeout(() => {
            newFlower.x = targetX
            newFlower.y = targetY
        }, 10)
    }
  }, interval)
}

function sureYes() {
  closeDialog()
  flowerExplosion()
}

const runawayOffset = ref({ x: 0, y: 0 })
const runawayRef = ref<HTMLButtonElement>()

function moveRunaway() {
  const dialog = dialogRef.value
  const btn = runawayRef.value
  if (!dialog || !btn) return

  const dialogRect = dialog.getBoundingClientRect()
  const btnRect = btn.getBoundingClientRect()

  const padding = 16
  const minX = dialogRect.left + padding - (btnRect.left - runawayOffset.value.x)
  const maxX = dialogRect.right - padding - btnRect.width - (btnRect.left - runawayOffset.value.x)
  const minY = dialogRect.top + padding - (btnRect.top - runawayOffset.value.y)
  const maxY = dialogRect.bottom - padding - btnRect.height - (btnRect.top - runawayOffset.value.y)

  const x = minX + Math.random() * (maxX - minX)
  const y = minY + Math.random() * (maxY - minY)
  runawayOffset.value = { x, y }
}

function sureNo() {
  dialogStep.value = 'ask'
  runawayOffset.value = { x: 0, y: 0 }
  riseFlowers()
}

// Random positioning with collision detection
interface FlowerPosition {
  x: number
  y: number
  image: string
  index: number
}

const flowerSize = computed(() => isMobile.value ? 150 : 250)
const minDistance = computed(() => flowerSize.value * 0.9) // Flowers can be close but not overlapping

function generateRandomPositions(): FlowerPosition[] {
  const positions: FlowerPosition[] = []
  const maxAttempts = 1000
  const targetCount = Math.floor((width.value * height.value) / (flowerSize.value * flowerSize.value * 2))
  
  for (let i = 0; i < targetCount; i++) {
    let attempts = 0
    let validPosition = false
    let x = 0
    let y = 0
    
    while (!validPosition && attempts < maxAttempts) {
      // Random position with padding from edges
      x = Math.random() * (width.value - flowerSize.value)
      y = Math.random() * (height.value - flowerSize.value)
      
      // Check collision with existing flowers
      validPosition = positions.every(pos => {
        const dx = pos.x - x
        const dy = pos.y - y
        const distance = Math.sqrt(dx * dx + dy * dy)
        return distance >= minDistance.value
      })
      
      attempts++
    }
    
    if (validPosition) {
      positions.push({
        x,
        y,
        image: images[Math.floor(Math.random() * images.length)] as string,
        index: i
      })
    }
  }
  
  return positions
}

const flowers = ref<FlowerPosition[]>([])

function regenerateFlowers() {
  flowers.value = generateRandomPositions()
}

// Generate flowers on mount and window resize
onMounted(() => {
  regenerateFlowers()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
})

// Regenerate when window size changes
function onResize() {
  width.value = window.innerWidth
  height.value = window.innerHeight
  regenerateFlowers()
}

const totalCells = computed(() => flowers.value.length)
const specialCell = computed(() => Math.floor(Math.random() * totalCells.value))
const partyCell = computed(() => {
  let cell
  do {
    cell = Math.floor(Math.random() * totalCells.value)
  } while (cell === specialCell.value)
  return cell
})

const containerStyle = computed(() => ({
  backgroundImage: `url(${meadowBg})`,
}))
</script>

<style scoped lang="scss">
.container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
  transition: background-color 5s ease;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  &.party-mode {
    animation: strobe 0.3s infinite;
  }

  &.falling {
    background-color: #1a1a1a;
  }
}

@keyframes strobe {
  0% { background-color: black; }
  50% { background-color: white; }
  100% { background-color: black; }
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.3); }
}

@keyframes pulse-icon {
  0%, 100% { transform: translate(-50%, -50%) scale(1); filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.5)); }
  50% { transform: translate(-50%, -50%) scale(1.3); filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.9)); }
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 8px rgba(255, 100, 150, 0.4); }
  50% { box-shadow: 0 0 20px rgba(255, 100, 150, 0.8); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes fall {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  70% {
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(45deg);
    opacity: 0;
  }
}

@keyframes rise {
  0% {
    transform: translateY(100vh) rotate(45deg);
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  100% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
}

.cell {
  position: absolute;
  cursor: pointer;
  transition: left 1s ease-out, top 1s ease-out;

  &.special {
    position: relative;
    cursor: pointer;

    &::after {
      content: '💖';
      position: absolute;
      top: 50%;
      left: 50%;
      font-size: 48px;
      line-height: 1;
      filter: drop-shadow(0 0 5px rgba(255, 100, 150, 0.8));
      animation: pulse-icon 1.5s ease-in-out infinite;
      z-index: 10;
      pointer-events: none;

      @media (max-width: 767px) {
        font-size: 32px;
      }
    }
  }

  &.party {
    position: relative;
    cursor: pointer;

    &::after {
      content: '🎵';
      position: absolute;
      top: 50%;
      left: 50%;
      font-size: 48px;
      line-height: 1;
      filter: drop-shadow(0 0 5px rgba(150, 100, 255, 0.8));
      animation: pulse-icon 1.5s ease-in-out infinite;
      z-index: 10;
      pointer-events: none;

      @media (max-width: 767px) {
        font-size: 32px;
      }
    }
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 1.5s ease;
  }

  &:hover img {
    transform: rotate(360deg);
  }

  &.rotated img {
    transform: rotate(360deg);
  }

  .party-mode & img {
    animation: spin 1s linear infinite;
  }

  .falling & {
    animation: fall 1.5s ease-in forwards;
  }

  .rising & {
    opacity: 0;
    transform: translateY(100vh);
    animation: rise 1.5s ease-out forwards;
  }
}

.flower-dialog {
  border: 1px solid rgba(255, 255, 255, 0.3);
  height: 300px;
  width: 500px;
  border-radius: 24px;
  padding: 3rem 4rem;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 2.2rem;
  letter-spacing: 0.02em;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  outline: none;
  position: relative;

  @media (max-width: 767px) {
    width: 85vw;
    height: 250px;
    padding: 2rem 1.5rem;
    font-size: 1.5rem;
    border-radius: 18px;
  }
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #fff;
  font-size: 1.8rem;
  cursor: url('@/assets/cursors/hover_32.png'), pointer;
  line-height: 1;
  padding: 0;
  opacity: 0.7;
  transition: opacity 0.2s;

  &:hover {
    opacity: 1;
  }

  &:focus {
    outline: none;
  }
}

.dialog-buttons {
  display: flex;
  gap: 1rem;
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
}

.fall-button {
  font-family: 'Poppins', sans-serif;
  font-weight: 400;
  font-size: 1rem;
  padding: 0.7rem 1.5rem;

  @media (max-width: 767px) {
    font-size: 0.85rem;
    padding: 0.6rem 1.2rem;
  }
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: #fff;
  cursor: url('@/assets/cursors/hover_32.png'), pointer;
  transition: background 0.3s;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  &:focus {
    outline: none;
  }

  &.runaway {
    position: relative;
    transition: transform 0.2s ease;
  }
}
</style>
