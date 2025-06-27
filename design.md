# Design System Guidelines

This document outlines the design rules and system guidelines for the visual identity.

## 1. Colors

The color palette is bold, clean, and incorporates subtle Canadian branding.

- **Primary – Deep Navy Blue**: `#000435`
  - Usage: Headers, navigation bars, buttons, primary text highlights.
- **Secondary – Sky Blue**: `#61B0F6`
  - Usage: Title banner backgrounds, callouts, visual accents.
- **Accent – Maple Red**: `#FB2000`
  - Usage: Selectively in the maple leaf icon, emphasis elements.
- **Background – Light Gray**: `#F2F2F2`
  - Usage: Page sections to create contrast with white and improve readability.
- **Text – Rich Charcoal**: `#272625`
  - Usage: Paragraph and general body text.

**Accessibility**: All color combinations must meet WCAG AA contrast ratios. Avoid gradients and drop shadows.

## 2. Typography

The primary font is **Kumbh Sans**, a modern geometric Google Font.

- **Font Family**: `'Kumbh Sans', sans-serif`
- **CDN Link**: `<link href="https://fonts.googleapis.com/css2?family=Kumbh+Sans:wght@400;600;700;900&display=swap" rel="stylesheet">`
- **Base Font Size**: `16px` (for `rem` calculations)

### Headings

- **Hero Title (display-H1)**:
  - Font size: `3rem` (48px)
  - Weight: `900`
  - Transform: Uppercase
  - Color: `#000435`
  - Line-height: 1.2
- **H1**:
  - Font size: `2.375rem` (38px)
  - Weight: `900`
  - Transform: Uppercase
  - Color: `#000435`
  - Line-height: 1.3
- **H2**:
  - Font size: `1.625rem` (26px)
  - Weight: `700`
  - Transform: Uppercase
  - Color: `#000435`
  - Line-height: 1.4
- **H3**:
  - Font size: `1.375rem` (22px)
  - Weight: `700`
  - Transform: Uppercase
  - Color: `#000435`
  - Line-height: 1.4

### Paragraph Text

- **P**:
  - Font size: `1rem` (16px)
  - Weight: `400`
  - Color: `#272625`
  - Line-height: 1.6
  - Max-width: `700px`

### Small Text

- Font size: `0.875rem` (14px)
- Weight: `600`
- Color: `#272625`

## 3. Layout

The layout is structured, flexible, and responsive.

### Grid & Structure

- **Max Container Width**: `1280px`
- **Content Horizontal Padding**:
  - Mobile: `1.875rem` (30px)
  - Tablet & Desktop: `3.75rem` (60px)
- **Section Padding (Top & Bottom)**:
  - Mobile: `3rem` (48px)
  - Desktop: `5rem` (80px)
- **Grid Columns**:
  - Desktop: Up to 3 columns
  - Mobile: 1 column
- **Gutter**: `1.5rem` (24px)

### Backgrounds & Spacing

- **Default Page Background**: `#F2F2F2`
- **Content Blocks Background**: `#FFFFFF`
- **Border Radius**: `0` (none)
- **Box Shadow**: None; separation is managed with spacing and contrast.

## 4. Buttons

Buttons are squared, minimal, with uppercase bold text.

### Base Rules

- **Font**: `Kumbh Sans`, `0.875rem` (14px), `700`, Uppercase
- **Padding**: `12px 24px`
- **Letter Spacing**: `0.05em`
- **Border Radius**: `0`
- **Icon**: Optional arrow (`→`) on the right.

### Variants

- **Primary (Outlined)**:
  - Text Color: `#000435`
  - Border: `1px solid #000435`
  - Background: `transparent`
  - Hover: Background `#F2F2F2`
- **Secondary (Filled)**:
  - Text Color: `#000435`
  - Background: `#61B0F6`
  - Hover: Background `#4C9AE0`
- **Disabled**:
  - Text Color: `#999999`
  - Border: `1px solid #CCCCCC`
  - Background: `#EDEDED`
  - Cursor: `not-allowed`
  - Opacity: `0.6`

## 5. Links & Interactive Elements

### Text Links

- **Font Size**: `1rem` (16px)
- **Weight**: `400`
- **Color**: `#61B0F6`
- **Hover & Active**: Color `#FB2000`, `text-decoration: underline`, `font-weight: 600`

### Navigation Links

- **Font Size**: `0.875rem` (14px)
- **Transform**: Uppercase
- **Weight**: `700`
- **Base Color**: `#61B0F6`
- **Hover/Active**: Color `#FB2000`, `text-decoration: underline`

### Navigation Behavior

- **Menu Type**: Hamburger menu on all screen sizes.
- **Menu Background**: `#000435`
- **Menu Text Color**: `#FFFFFF`
- **Active Link Color**: `#FB2000`
- **Menu Height**: Full screen (`100vh`)
- **Layout**: Vertical stacked, close icon top-right.

### Focus Styles

- **Outline**: `2px solid #61B0F6`
- **Outline Offset**: `2px`

## 6. Cards & Containers

- **Background**: `#FFFFFF`
- **Padding**:
  - Mobile: `1.5rem` (24px)
  - Desktop: `2.5rem` (40px)
- **Border Radius**: `0`
- **Box Shadow**: None
- **Margin Bottom (between cards)**: `32px`

### Variants

- **Standard Card**: Clean white block.
- **Image Card**: Image top or side, content aligned.
- **Callout Block**: Background `#F2F2F2`.

## 7. Forms

- **Font**: `Kumbh Sans`
- **Input Text Size**: `1rem` (16px)
- **Input Padding**: `12px 16px`
- **Border**: `1px solid #CCCCCC`
- **Border Radius**: `0`
- **Background**: `#FFFFFF`
- **Focus**: Border color `#61B0F6`, `outline: 2px solid #61B0F6`
- **Labels**:
  - Font size: `0.875rem` (14px)
  - Weight: Bold (`700`)
  - Color: `#000435`
  - Position: Above input
- **Error State**: Border color `#FB2000`, text color `#FB2000`
- **Submit Buttons**: Follow standard button styles.

## 8. Icons & Visual Elements

### Icons

- **Style**: Stroke icons (not filled)
- **Color**: Context-dependent
  - In text: `#000435`
  - In alerts/callouts: `#61B0F6` or `#FB2000`
- **Size**: `16px – 32px`
- **Spacing**: `8px` from text

### Maple Leaf Icon

- **Usage**: Decorative accent, not for functional UI.
- **Color**: `#FB2000`
- **Format**: SVG preferred.

### Dividers

- **Color**: `#DCDCDC`
- **Thickness**: `1px`
- **Usage**: Subtle section separation.

## 9. Decorative Elements

### Wave Separator

- **Usage**: Visual separator under headings in some blocks.
- **Type**: SVG
- **Color**: `#000435`
- **Width**: Fixed, approximately `80px – 100px`
- **Spacing**: `16px` above and below.
- **Frequency**: One wave per block only.
