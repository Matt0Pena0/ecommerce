/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2023 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
  'use strict'

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  const setTheme = theme => {
    if (theme === 'auto') {
      document.documentElement.setAttribute(
        'data-bs-theme',
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      )
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  setTheme(getPreferredTheme())

  const showActiveTheme = (theme, focus = false) => {
    const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
    if (!btnToActive) return

    const svgOfActiveBtn = btnToActive.querySelector('svg use').getAttribute('href')

    // Reset todos los botones
    document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
      element.classList.remove('active')
      element.setAttribute('aria-pressed', 'false')
    })

    // Activar el actual
    btnToActive.classList.add('active')
    btnToActive.setAttribute('aria-pressed', 'true')

    // Actualizar todos los íconos activos
    document.querySelectorAll('.theme-icon-active use').forEach(icon => {
      icon.setAttribute('href', svgOfActiveBtn)
    })

    // Actualizar todos los textos
    document.querySelectorAll('#bd-theme-text').forEach(node => {
      node.textContent = theme.charAt(0).toUpperCase() + theme.slice(1)
    })

    // Actualizar aria-labels
    document.querySelectorAll('#bd-theme').forEach(switcher => {
      const textNode = switcher.querySelector('#bd-theme-text')
      const labelText = textNode ? textNode.textContent : ''
      const themeSwitcherLabel = `${labelText} (${btnToActive.dataset.bsThemeValue})`
      switcher.setAttribute('aria-label', themeSwitcherLabel)
      if (focus) switcher.focus()
    })
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme())
    }
  })

  window.addEventListener('DOMContentLoaded', () => {
    showActiveTheme(getPreferredTheme())

    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(toggle => {
        toggle.addEventListener('click', () => {
          const theme = toggle.getAttribute('data-bs-theme-value')
          setStoredTheme(theme)
          setTheme(theme)
          showActiveTheme(theme, true)
        })
      })
  })
})()
