---
name: Academic Portal Modern
colors:
  surface: '#faf8ff'
  surface-dim: '#d9d9e4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3fe'
  surface-container: '#ededf8'
  surface-container-high: '#e7e7f2'
  surface-container-highest: '#e1e2ed'
  on-surface: '#191b23'
  on-surface-variant: '#424654'
  inverse-surface: '#2e3038'
  inverse-on-surface: '#f0f0fb'
  outline: '#737786'
  outline-variant: '#c3c6d7'
  surface-tint: '#0056d2'
  primary: '#0054cd'
  on-primary: '#ffffff'
  primary-container: '#2e6dec'
  on-primary-container: '#fefcff'
  inverse-primary: '#b2c5ff'
  secondary: '#006876'
  on-secondary: '#ffffff'
  secondary-container: '#58e6ff'
  on-secondary-container: '#006573'
  tertiary: '#934600'
  on-tertiary: '#ffffff'
  tertiary-container: '#b95a00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b2c5ff'
  on-primary-fixed: '#001847'
  on-primary-fixed-variant: '#0040a1'
  secondary-fixed: '#a1efff'
  secondary-fixed-dim: '#44d8f1'
  on-secondary-fixed: '#001f25'
  on-secondary-fixed-variant: '#004e59'
  tertiary-fixed: '#ffdbc7'
  tertiary-fixed-dim: '#ffb688'
  on-tertiary-fixed: '#311300'
  on-tertiary-fixed-variant: '#733500'
  background: '#faf8ff'
  on-background: '#191b23'
  surface-variant: '#e1e2ed'
  crimson-header: '#e01a3f'
  surface-base: '#ecf0f5'
  surface-white: '#ffffff'
  text-dark: '#373a3c'
  text-muted: '#999999'
  accent-purple: '#8153fe'
  accent-green: '#9ccc65'
  accent-red: '#ff5252'
  navy-badge: '#101b33'
typography:
  display:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 19px
    fontWeight: '600'
    lineHeight: 26px
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
  title-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  body-lg:
    fontFamily: Open Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-md:
    fontFamily: Open Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  body-sm:
    fontFamily: Open Sans
    fontSize: 10px
    fontWeight: '400'
    lineHeight: 14px
  label-sm:
    fontFamily: Inter
    fontSize: 9px
    fontWeight: '600'
    lineHeight: 12px
    letterSpacing: 0.5px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 14px
  margin: 21px
  space-xs: 7px
  space-sm: 14px
  space-md: 21px
  space-lg: 28px
  space-xl: 42px
---

# Design System Inspired by Welcome

> Auto-extracted from `https://situ-kem.telkomuniversity.ac.id/tak/home` on 2026-10-31

## 1. Visual Theme & Atmosphere

High-contrast dark mode with vivid accents — feels modern, technical, and focused.

**Key Characteristics:**
- Inter as the heading font
- Open Sans as the body font for all running text
- Dark background (#e01a3f) as the primary canvas
- Primary accent `#4680ff` used for CTAs and brand highlights
- 4 shadow level(s) detected — tinted shadows
- Rounded corners (3px+) creating a friendly, approachable feel
- Tags: dark, rounded, colorful, compact, sans-serif

## 2. Color Palette & Roles

### Primary
- **Primary Accent** (`#4680ff`) · `--color-primary`: Brand color, CTA backgrounds, link text, interactive highlights.
- **Secondary Accent** (`#00bcd4`) · `--color-secondary`: Secondary brand, hover states, complementary highlights.
- **Background** (`#e01a3f`) · `--color-bg`: Page background, primary canvas.
- **Background Secondary** (`#ecf0f5`) · `--color-bg-secondary`: Cards, surfaces, alternating sections.

### Text
- **Text Primary** (`#373a3c`) · `--color-text`: Headings and body text.
- **Text Secondary** (`#999999`) · `--color-text-secondary`: Muted text, captions, placeholders.

### Borders & Surfaces
- **Border** (`#ecf0f5`) · `--color-border`: Dividers, outlines, input borders.

### Full Extracted Palette

| # | Hex | CSS Variable | Role | Area | Contrast |
|---|---|---|---|---|---|
| 1 | `#ffffff` | `--palette-1` | block | large | text-dark |
| 2 | `#ecf0f5` | `--palette-2` | block | large | text-dark |
| 3 | `#ff5252` | `--palette-3` | button | small | text-dark |
| 4 | `#4680ff` | `--palette-4` | text-accent | small | text-light |
| 5 | `#00bcd4` | `--palette-5` | badge | small | text-dark |
| 6 | `#8153fe` | `--palette-6` | badge | small | text-light |
| 7 | `#9ccc65` | `--palette-7` | badge | small | text-dark |
| 8 | `#101b33` | `--palette-8` | badge | small | text-light |
| 9 | `#e01a3f` | `--palette-9` | text-accent | small | text-light |

## 3. Typography Rules

- **Heading Font:** `Inter`, sans-serif
- **Body Font:** `Open Sans` (web font)

### Type Scale
| Token | Size | Suggested Usage |
|---|---|---|
| Display | `28px` | headings |
| H1 | `24px` | headings |
| H2 | `19.2px` | headings |
| H3 | `16px` | headings |
| H4 | `14px` | headings |
| Body L | `13px` | body / supporting text |
| Body | `10px` | body / supporting text |
| Small | `9px` | body / supporting text |

## 4. Component Stylings

### Primary Button
```css
.btn-primary {
  background: transparent;
  color: #535763;
  border-radius: 8px;
  padding: 7px 10px;
  font-size: 14px;
  font-weight: 400;
  border: none;
  cursor: pointer;
}
```

### Card
```css
.card {
  background: #ffffff;
  border-radius: 8px;
  padding: 0px;
  box-shadow: rgba(0, 0, 0, 0.075) 0px 2px 4px 0px;
}
```

## 5. Layout Principles
- **Base spacing unit:** `7px` — use multiples (14px, 21px, 28px, etc.)
- **Border Radius:** `8px` buttons, `8px` cards, subtle `3px`-`4px`.
