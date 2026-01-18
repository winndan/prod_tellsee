/* ========================================
   CLARITY ENGINE - Landing Page Scripts
   Vanilla JavaScript - No Dependencies
======================================== */

;(() => {
  /* ----------------------------------------
     SCROLL PROGRESS BAR
  ---------------------------------------- */
  function initScrollProgress() {
    const progressBar = document.getElementById("scroll-progress-bar")
    if (!progressBar) return

    function updateProgress() {
      const scrollTop = window.scrollY
      const docHeight = document.documentElement.scrollHeight - window.innerHeight
      const progress = (scrollTop / docHeight) * 100
      progressBar.style.width = `${Math.min(progress, 100)}%`
    }

    window.addEventListener("scroll", updateProgress, { passive: true })
    updateProgress()
  }

  /* ----------------------------------------
     MOBILE NAVIGATION
  ---------------------------------------- */
  function initMobileNav() {
    const toggle = document.getElementById("nav-toggle")
    const navLinks = document.getElementById("nav-links")
    if (!toggle || !navLinks) return

    toggle.addEventListener("click", () => {
      toggle.classList.toggle("active")
      navLinks.classList.toggle("active")
      document.body.style.overflow = navLinks.classList.contains("active") ? "hidden" : ""
    })

    // Close menu when clicking a link
    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        toggle.classList.remove("active")
        navLinks.classList.remove("active")
        document.body.style.overflow = ""
      })
    })

    // Close menu on escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navLinks.classList.contains("active")) {
        toggle.classList.remove("active")
        navLinks.classList.remove("active")
        document.body.style.overflow = ""
      }
    })
  }

  /* ----------------------------------------
     TYPING EFFECT
  ---------------------------------------- */
  function initTypingEffect() {
    const typingElement = document.getElementById("typing-text")
    if (!typingElement) return

    const text = "Clarity Over Chaos"
    let index = 0

    function type() {
      if (index <= text.length) {
        typingElement.textContent = text.slice(0, index)
        index++
        setTimeout(type, 80)
      }
    }

    // Start typing after a short delay
    setTimeout(type, 500)
  }

  /* ----------------------------------------
     PARTICLE SYSTEM
  ---------------------------------------- */
  function initParticles() {
    const container = document.getElementById("particles")
    if (!container) return

    const particleCount = window.innerWidth < 768 ? 15 : 30

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement("div")
      particle.className = "particle"
      particle.style.cssText = `
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation-delay: ${Math.random() * 6}s;
        animation-duration: ${4 + Math.random() * 4}s;
        opacity: ${0.1 + Math.random() * 0.3};
        width: ${2 + Math.random() * 4}px;
        height: ${2 + Math.random() * 4}px;
      `
      container.appendChild(particle)
    }
  }

  /* ----------------------------------------
     SMOOTH SCROLL FOR ANCHOR LINKS
  ---------------------------------------- */
  function initSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]')

    anchorLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        const targetId = this.getAttribute("href")
        if (targetId === "#") return

        const targetElement = document.querySelector(targetId)
        if (targetElement) {
          e.preventDefault()
          const navHeight = document.querySelector(".nav").offsetHeight
          const targetPosition = targetElement.offsetTop - navHeight - 20

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          })
        }
      })
    })
  }

  /* ----------------------------------------
     FADE-IN ON SCROLL ANIMATION
  ---------------------------------------- */
  function initFadeInOnScroll() {
    const fadeElements = document.querySelectorAll(".fade-in")

    const observerOptions = {
      root: null,
      rootMargin: "0px 0px -80px 0px",
      threshold: 0.1,
    }

    function handleIntersection(entries, observer) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const element = entry.target
          const delay = Number.parseInt(getComputedStyle(element).getPropertyValue("--delay") || 0)

          setTimeout(() => {
            element.classList.add("visible")

            // Animate confidence bar when visible
            const confidenceFill = element.querySelector(".animate-fill")
            if (confidenceFill) {
              const width = confidenceFill.dataset.width || 87
              confidenceFill.style.setProperty("--fill-width", `${width}%`)
              confidenceFill.classList.add("animated")
            }
          }, delay * 100)

          observer.unobserve(element)
        }
      })
    }

    const observer = new IntersectionObserver(handleIntersection, observerOptions)
    fadeElements.forEach((element) => observer.observe(element))
  }

  /* ----------------------------------------
     TILT CARD EFFECT
  ---------------------------------------- */
  function initTiltCards() {
    const cards = document.querySelectorAll(".tilt-card")

    // Skip on touch devices
    if ("ontouchstart" in window) return

    cards.forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
        const centerX = rect.width / 2
        const centerY = rect.height / 2

        const rotateX = ((y - centerY) / centerY) * -5
        const rotateY = ((x - centerX) / centerX) * 5

        card.style.setProperty("--rotate-x", `${rotateX}deg`)
        card.style.setProperty("--rotate-y", `${rotateY}deg`)
      })

      card.addEventListener("mouseleave", () => {
        card.style.setProperty("--rotate-x", "0deg")
        card.style.setProperty("--rotate-y", "0deg")
      })
    })
  }

  /* ----------------------------------------
     CTA BUTTON INTERACTIONS
  ---------------------------------------- */
// function initCTAButtons() {
//   const primaryCTA = document.getElementById("cta-primary")
//   const finalCTA = document.getElementById("cta-final-btn")

//   function handleCTAClick() {
//     showNotification("Thanks for your interest!.")
//     // ✅ allow normal href navigation
//   }

//   if (primaryCTA) primaryCTA.addEventListener("click", handleCTAClick)
//   if (finalCTA) finalCTA.addEventListener("click", handleCTAClick)
// }


  /* ----------------------------------------
     NOTIFICATION SYSTEM
  ---------------------------------------- */
  function showNotification(message) {
    const existingNotification = document.querySelector(".notification")
    if (existingNotification) existingNotification.remove()

    const notification = document.createElement("div")
    notification.className = "notification"
    notification.innerHTML = `
      <div class="notification-content">
        <span class="notification-icon">◇</span>
        <p>${message}</p>
        <button class="notification-close" aria-label="Close notification">&times;</button>
      </div>
    `

    // Responsive positioning
    const isMobile = window.innerWidth < 480
    notification.style.cssText = `
      position: fixed;
      bottom: ${isMobile ? "16px" : "24px"};
      ${isMobile ? "left: 16px; right: 16px;" : "right: 24px;"}
      z-index: 1000;
      animation: slideIn 0.3s ease;
    `

    const content = notification.querySelector(".notification-content")
    content.style.cssText = `
      display: flex;
      align-items: center;
      gap: 12px;
      background-color: #161618;
      border: 1px solid #3b82f6;
      border-radius: 12px;
      padding: 16px 20px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(59, 130, 246, 0.2);
    `

    const icon = notification.querySelector(".notification-icon")
    icon.style.cssText = `
      color: #3b82f6;
      font-size: 1.25rem;
      flex-shrink: 0;
    `

    const text = notification.querySelector("p")
    text.style.cssText = `
      color: #fafafa;
      font-size: 0.95rem;
      margin: 0;
      flex: 1;
    `

    const closeBtn = notification.querySelector(".notification-close")
    closeBtn.style.cssText = `
      background: none;
      border: none;
      color: #71717a;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0;
      margin-left: 8px;
      line-height: 1;
      flex-shrink: 0;
      transition: color 0.15s ease;
    `

    closeBtn.addEventListener("mouseenter", () => (closeBtn.style.color = "#fafafa"))
    closeBtn.addEventListener("mouseleave", () => (closeBtn.style.color = "#71717a"))

    // Add animation keyframes if not already added
    if (!document.querySelector("#notification-styles")) {
      const style = document.createElement("style")
      style.id = "notification-styles"
      style.textContent = `
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideOut {
          from { opacity: 1; transform: translateY(0); }
          to { opacity: 0; transform: translateY(20px); }
        }
      `
      document.head.appendChild(style)
    }

    document.body.appendChild(notification)

    function dismissNotification() {
      notification.style.animation = "slideOut 0.3s ease forwards"
      setTimeout(() => notification.remove(), 300)
    }

    closeBtn.addEventListener("click", dismissNotification)
    setTimeout(() => {
      if (document.body.contains(notification)) dismissNotification()
    }, 5000)
  }

  /* ----------------------------------------
     NAV SCROLL EFFECT
  ---------------------------------------- */
  function initNavScrollEffect() {
    const nav = document.querySelector(".nav")
    if (!nav) return

    let ticking = false

    function updateNav() {
      const scrollY = window.scrollY

      if (scrollY > 50) {
        nav.classList.add("scrolled")
      } else {
        nav.classList.remove("scrolled")
      }

      ticking = false
    }

    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          requestAnimationFrame(updateNav)
          ticking = true
        }
      },
      { passive: true },
    )
  }

  /* ----------------------------------------
     INITIALIZE ALL SCRIPTS
  ---------------------------------------- */
  function init() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initAll)
    } else {
      initAll()
    }
  }

  function initAll() {
    initScrollProgress()
    initMobileNav()
    initTypingEffect()
    initParticles()
    initSmoothScroll()
    initFadeInOnScroll()
    initTiltCards()
    initCTAButtons()
    initNavScrollEffect()
  }

  init()
})()
