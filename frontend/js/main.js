class Dashboard {
  constructor() {
    this.config = {
      apiBase: '/api',
      refreshInterval: 30000
    }
    this.init()
  }

  init() {
    this.loadData()
    this.initAnimations()
    this.setupEventListeners()
  }

  async loadData() {
    try {
      const uni = this.getUniversity()
      const response = await fetch(`${this.config.apiBase}/${uni}`)
      this.updateUI(await response.json())
    } catch (error) {
      console.error('数据加载失败:', error)
      this.showFallbackData()
    }
  }

  getUniversity() {
    return document.body.classList.contains('anu-container') ? 'anu' :
           document.body.classList.contains('sydney-container') ? 'sydney' : 'unsw'
  }

  initAnimations() {
    this.animateNumbers()
    this.initProgressBars()
    this.startCountdowns()
  }

  animateNumbers() {
    document.querySelectorAll('.stat-value').forEach(el => {
      const target = parseFloat(el.textContent)
      let current = 0
      const step = target / 30
      
      const animate = () => {
        current += step
        if (current >= target) {
          el.textContent = target % 1 === 0 ? target : target.toFixed(1)
          return
        }
        el.textContent = current % 1 === 0 ? current : current.toFixed(1)
        requestAnimationFrame(animate)
      }
      requestAnimationFrame(animate)
    })
  }

  initProgressBars() {
    document.querySelectorAll('.progress-bar').forEach(bar => {
      const width = parseFloat(bar.style.width)
      bar.style.width = '0'
      setTimeout(() => bar.style.width = `${width}%`, 100)
    })
  }

  startCountdowns() {
    document.querySelectorAll('.deadline').forEach(el => {
      let hours = parseInt(el.dataset.hours)
      const update = () => {
        el.textContent = `剩余${hours}小时`
        el.style.color = hours <= 3 ? 'var(--danger-red)' : 'var(--secondary-blue)'
        hours > 0 ? hours-- : clearInterval(timer)
      }
      const timer = setInterval(update, 3600000)
      update()
    })
  }
}

document.addEventListener('DOMContentLoaded', () => new Dashboard())