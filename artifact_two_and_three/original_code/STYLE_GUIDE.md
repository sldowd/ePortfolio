# Grazioso Salvare Dashboard - Frontend Style Guide

## Overview

This style guide documents the design system, color palette, typography, and component styling for the Grazioso Salvare Animal Shelter Dashboard. It serves as a reference for maintaining visual consistency and extending the application's user interface.

**Design Philosophy:** Professional, warm, and accessible interface that puts data clarity first while reflecting the Grazioso Salvare brand identity.

---

## Table of Contents

1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Component Styles](#component-styles)
4. [Layout & Spacing](#layout--spacing)
5. [Interactive States](#interactive-states)
6. [Responsive Design](#responsive-design)
7. [Accessibility](#accessibility)
8. [Code Examples](#code-examples)

---

## Color Palette

### Primary Colors

```python
COLORS = {
    # Brand Colors
    'brand_red': '#c9341b',           # Grazioso Salvare logo red
    'dark_slate': '#2c3e50',          # Primary headers and emphasis
    
    # Background Colors
    'page_background': '#F2E6E3',     # Main page background (warm beige)
    'card_background': '#faf8f5',     # Card and elevated surfaces
    'table_data_bg': '#faf8f5',       # Data table row background
    
    # Text Colors
    'text_primary': '#212529',        # Main body text
    'text_secondary': '#6c757d',      # Secondary text, captions
    'text_muted': '#6c757d',          # Muted text (attributions, metadata)
    'text_on_dark': '#ffffff',        # Text on dark backgrounds
    
    # Interactive Elements
    'radio_accent': '#c9341b',        # Radio buttons, checkboxes
    'link_color': '#c9341b',          # Hyperlinks
    
    # Borders & Lines
    'border_light': '#ffffff',        # Light borders (chart slices)
    'border_default': '#dee2e6',      # Standard borders
}
```

### Color Usage Guidelines

**Brand Red (#c9341b)**
- ✅ Use for: Radio buttons, links, important CTAs, logo
- ❌ Avoid for: Large background areas, body text, table headers
- **Rationale:** High saturation works as accent but overwhelms when overused

**Dark Slate (#2c3e50)**
- ✅ Use for: Headers, dropdown card backgrounds, table headers
- ❌ Avoid for: Body text, large content areas
- **Rationale:** Professional, high contrast, readable on light backgrounds

**Warm Neutrals (#F2E6E3, #faf8f5)**
- ✅ Use for: Page backgrounds, card surfaces, table cells
- ❌ Avoid for: Text (insufficient contrast)
- **Rationale:** Soft, warm tones reduce eye strain and complement brand red

### Color Contrast Ratios

Following WCAG 2.1 Level AA standards:

| Foreground | Background | Ratio | Rating |
|------------|-----------|-------|--------|
| #212529 (text) | #F2E6E3 (page) | 8.2:1 | ✅ AAA |
| #ffffff (text) | #2c3e50 (header) | 12.6:1 | ✅ AAA |
| #c9341b (link) | #F2E6E3 (page) | 4.8:1 | ✅ AA |
| #212529 (text) | #faf8f5 (card) | 11.9:1 | ✅ AAA |

---

## Typography

### Font Family

**Primary Font:** Ubuntu  
**Fallback Stack:** `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`

```python
font_family = '"Ubuntu", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
```

**Rationale:**
- Ubuntu provides friendly, modern aesthetic
- Excellent readability at dashboard data densities
- Loaded automatically via Bootstrap UNITED theme
- System font fallbacks ensure cross-platform consistency

### Font Sizes & Weights

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| H1 | 2.5rem (40px) | 700 (Bold) | 1.2 | Page title |
| H2 | 2rem (32px) | 700 (Bold) | 1.2 | Section headers |
| H3 | 1.75rem (28px) | 600 (Semibold) | 1.3 | Subsection headers |
| H4 | 1.5rem (24px) | 600 (Semibold) | 1.3 | Card titles |
| H5 | 1.25rem (20px) | 600 (Semibold) | 1.4 | Component labels |
| Body | 1rem (16px) | 400 (Regular) | 1.5 | Paragraph text |
| Small | 0.875rem (14px) | 400 (Regular) | 1.4 | Captions, metadata |
| Table Header | 1rem (16px) | 700 (Bold) | 1.3 | Column headers |
| Table Data | 0.9375rem (15px) | 400 (Regular) | 1.4 | Table cells |

### Typography Best Practices

1. **Never use more than 3 font sizes in a single component**
2. **Maintain 1.5x line height minimum for body text** (accessibility)
3. **Use bold weight sparingly** (headers, emphasis only)
4. **Avoid all-caps for long text** (reduces readability)
5. **Keep line length 50-75 characters** for optimal reading

---

## Component Styles

### Welcome Card

**Purpose:** Introduce dashboard and provide usage instructions

```python
dbc.Card([
    dbc.CardBody([
        # Logo and text content
    ])
], 
style={'backgroundColor': '#faf8f5'},
className='shadow-sm mb-4 m-5'
)
```

**Styling Details:**
- Background: `#faf8f5` (warm off-white)
- Shadow: `shadow-sm` (subtle depth)
- Margin: `m-5` (5rem / 80px all sides)
- Border radius: 8px (inherited from Bootstrap)
- Padding: Default card body padding (1.25rem)

### Data Table

**Purpose:** Display paginated, sortable animal records

```python
dash_table.DataTable(
    style_cell={
        'textAlign': 'left',
        'height': 'auto',
        'minWidth': '90px',
        'width': '180px',
        'maxWidth': '180px',
        'textOverflow': 'ellipsis',
    },
    style_table={
        'overflowX': 'auto',
        'borderRadius': '8px'
    },
    style_data={
        'backgroundColor': '#faf8f5',
        'fontFamily': '"Ubuntu", sans-serif'
    },
    style_header={
        'color': 'white',
        'backgroundColor': '#2c3e50',
        'fontWeight': 'bold',
        'fontFamily': '"Ubuntu", sans-serif'
    }
)
```

**Styling Details:**
- Headers: Dark slate background, white text, bold weight
- Cells: Left-aligned, ellipsis overflow, warm background
- Borders: 8px rounded corners on table container
- Fixed column widths: Prevents layout shift during filtering
- Horizontal scroll: Handles overflow data gracefully

**Cell Width Strategy:**
- **Minimum:** 90px (prevents squishing on mobile)
- **Standard:** 180px (optimal for most text fields)
- **Maximum:** 180px (prevents excessive whitespace)

### Filter Dropdown

**Purpose:** Select rescue type to filter data

```python
dbc.Card([
    dbc.CardBody([
        html.H5('Filter by Rescue Type', className='card-title'),
        dcc.Dropdown(
            ['Water Rescue', 'Mountain Rescue', 'Disaster Rescue', 'Reset'],
            placeholder='Select Rescue Type',
            id='dropdown-filter',
            style={'color': '#2c3e50'}
        ),
    ], 
    style={
        'color': 'white',
        'backgroundColor': '#2c3e50',
        'borderRadius': '8px'
    },
    className='p-3')
])
```

**Styling Details:**
- Card background: Dark slate (#2c3e50)
- Card text: White for contrast
- Dropdown text: Dark slate (readable on white dropdown background)
- Border radius: 8px
- Padding: `p-3` (1rem / 16px all sides)

### Pie Chart

**Purpose:** Visualize breed distribution

```python
fig = px.pie(top_breeds, names='breed', values='count', title='Breed Distribution')

fig.update_traces(
    hovertemplate='<b>%{label}</b><br>Dogs Available: %{value}<br>Percentage: %{percent}<extra></extra>',
    textposition='inside',
    textinfo='percent',
    marker=dict(line=dict(color='white', width=2))
)

fig.update_layout(
    paper_bgcolor='#F2E6E3',
    font={'family': 'ubuntu'},
    title_font={'size': 22}
)
```

**Styling Details:**
- Background: Matches page background (#F2E6E3)
- Slice borders: 2px white lines for separation
- Title: 22px Ubuntu font
- Text: Percentages displayed inside slices
- Hover: Custom tooltip with breed, count, and percentage

**Chart Best Practices:**
- Limit to 8 slices maximum (prevents overcrowding)
- Use high-contrast color sequence (RdBu)
- White borders essential for distinguishing similar colors
- Interactive hover provides detailed data

### Bar Chart (Age Distribution)

**Purpose:** Visualize age distribution of filtered animals
```python
fig_bar = px.bar(
    age_distribution,
    x='age_group',
    y='count',
    title='Age Distribution',
    color_discrete_sequence=px.colors.sequential.RdBu
)

fig_bar.update_traces(
    hovertemplate='<b>%{x}</b><br>Animals: %{y}<extra></extra>',
    marker=dict(line=dict(color='white', width=2))
)

fig_bar.update_layout(
    paper_bgcolor='#F2E6E3',
    plot_bgcolor='#2c3e50',  # Dark background for contrast
    font={'family': 'ubuntu'},
    title_font={'size': 22},
    showlegend=False
)
```

**Styling Details:**
- Background: Page background color (#F2E6E3)
- Plot area: Dark slate background (#2c3e50) for high contrast
- Bar borders: 2px white lines
- Age bins: <6mo, 6-12mo, 1-2yr, 2-3yr, 3-4yr, 4-5yr, 5-6yr, 6+yr
- No legend (color serves aesthetic purpose only)

### Geolocation Map

**Purpose:** Show selected animal's shelter location

```python
dl.Map(
    style={'width': '100%', 'height': '500px'},
    center=[lat, lon],
    zoom=10,
    children=[
        dl.TileLayer(id="base-layer-id"),
        dl.Marker(
            position=[lat, lon],
            children=[
                dl.Tooltip(breed),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(name)
                ])
            ]
        )
    ]
)
```

**Styling Details:**
- Width: 100% (responsive to container)
- Height: 500px (matches pie chart height)
- Zoom: Level 10 (neighborhood scale)
- Dynamic center: Updates to selected animal's coordinates
- Marker: Default Leaflet marker (red pin)

**Map Interaction:**
- Hover: Tooltip shows breed
- Click: Popup reveals animal name
- Pan: User can explore surrounding area
- Zoom: Mouse wheel or controls

---

## Layout & Spacing

### Grid System

Dashboard uses **Bootstrap's 12-column grid system** via Dash Bootstrap Components.

**Breakpoints:**
- `xs`: <576px (mobile)
- `sm`: ≥576px (tablet)
- `md`: ≥768px (landscape tablet)
- `lg`: ≥992px (desktop)
- `xl`: ≥1200px (large desktop)

**Common Patterns:**

```python
# Two-column layout (chart and map side-by-side)
dbc.Row([
    dbc.Col([...], xs=12, md=6),  # Full width mobile, half width desktop
    dbc.Col([...], xs=12, md=6)
])

# Logo and text layout
dbc.Row([
    dbc.Col([...], xs=12, md=4),  # Logo: 1/3 width desktop
    dbc.Col([...], xs=12, md=8)   # Text: 2/3 width desktop
])
```

### Spacing Scale

Bootstrap spacing utilities (margin and padding):

| Class | Size | Pixels | Usage |
|-------|------|--------|-------|
| `m-0`, `p-0` | 0 | 0px | Remove default spacing |
| `m-1`, `p-1` | 0.25rem | 4px | Tight spacing |
| `m-2`, `p-2` | 0.5rem | 8px | Small spacing |
| `m-3`, `p-3` | 1rem | 16px | **Standard spacing (most common)** |
| `m-4`, `p-4` | 1.5rem | 24px | Medium spacing |
| `m-5`, `p-5` | 3rem | 48px | Large spacing (sections) |

**Direction Modifiers:**
- `t`: top
- `b`: bottom
- `s`: start (left in LTR)
- `e`: end (right in LTR)
- `x`: horizontal (left and right)
- `y`: vertical (top and bottom)

**Examples:**
- `mb-3`: Margin bottom 16px
- `px-4`: Padding left and right 24px
- `mt-5`: Margin top 48px

### Spacing Recommendations

**Between Sections:**
- Major sections: `mb-5` (48px)
- Minor sections: `mb-4` (24px)
- Related components: `mb-3` (16px)

**Within Cards:**
- Card body padding: `p-3` or `p-4`
- Between card elements: `mb-2` or `mb-3`

**Text Elements:**
- After headings: `mb-3`
- Between paragraphs: `mb-2`
- Above lists: `mb-2`

---

## Interactive States

### Hover States

**Data Table Rows:**
- Default: `#faf8f5` background
- Hover: Slightly darker shade (handled by DataTable component)

**Dropdown:**
- Default: White background
- Hover: Light gray background (#f8f9fa)
- Focus: Blue outline (browser default)

**Links:**
- Default: `#c9341b` (brand red)
- Hover: Darker red with underline
- Visited: Same as default (maintain consistency)

**Radio Buttons:**
- Unchecked: Light gray circle
- Checked: `#c9341b` filled circle
- Hover: Slight scale increase (subtle feedback)

### Focus States

**Accessibility Requirement:** All interactive elements must have visible focus indicators.

```css
/* Example focus styling */
*:focus {
    outline: 2px solid #2c3e50;
    outline-offset: 2px;
}
```

**Elements requiring focus states:**
- Dropdown menu
- Table rows
- Radio buttons
- Map controls
- Links

### Active/Selected States

**Selected Table Row:**
- Background: `#2c3e50` (dark slate)
- Color: white

**Active Filter:**
- Dropdown displays selected value
- Applied filter reflected in data table count

---

## Responsive Design

### Mobile-First Approach

Dashboard components adapt from mobile to desktop:

**Mobile (xs, <576px):**
- Single column layout
- Logo stacks above text
- Chart and map stack vertically
- Table scrolls horizontally
- Reduced padding/margins

**Tablet (md, ≥768px):**
- Two-column layout for chart/map
- Logo and text side-by-side
- Increased spacing

**Desktop (lg+, ≥992px):**
- Full layout with optimal spacing
- All columns at intended widths

### Responsive Component Patterns

**Fluid Container:**
```python
dbc.Container([...], fluid=True)  # Full width at all breakpoints
```

**Responsive Columns:**
```python
dbc.Col([...], xs=12, md=6, lg=4)  # Full mobile, half tablet, third desktop
```

**Conditional Visibility:**
```python
html.Div([...], className='d-none d-md-block')  # Hidden mobile, visible tablet+
```

### Testing Breakpoints

Ensure dashboard functions correctly at:
- 360px (smallest common mobile)
- 768px (tablet portrait)
- 1024px (tablet landscape)
- 1920px (desktop HD)

---

## Accessibility

### WCAG 2.1 Level AA Compliance

**Color Contrast:**
- All text meets minimum 4.5:1 ratio
- Large text (18pt+) meets 3:1 ratio
- Interactive elements distinguishable by more than color

**Keyboard Navigation:**
- All interactive elements accessible via Tab key
- Logical tab order follows visual flow
- Focus indicators clearly visible

**Screen Reader Support:**
- Semantic HTML structure (headers, lists, tables)
- Alt text for logo image
- Descriptive link text (avoid "click here")
- ARIA labels where needed

**Cognitive Accessibility:**
- Clear, concise language
- Consistent navigation patterns
- Predictable component behavior
- No auto-playing animations

### Accessibility Checklist

- [ ] All images have alt text or are marked decorative
- [ ] Color is not sole means of conveying information
- [ ] Sufficient contrast on all text
- [ ] Keyboard navigation works throughout
- [ ] Focus indicators visible on all interactive elements
- [ ] Form labels associated with inputs
- [ ] Error messages clearly communicated
- [ ] Responsive design works with zoom up to 200%

---

## Code Examples

### Complete Component Example

**Filter Card with Dropdown:**

```python
dbc.Card([
    dbc.CardBody([
        html.H5(
            'Filter by Rescue Type',
            className='card-title mb-3',
            style={'color': 'white'}
        ),
        dcc.Dropdown(
            options=[
                {'label': 'Water Rescue', 'value': 'Water Rescue'},
                {'label': 'Mountain/Wilderness Rescue', 'value': 'Mountain Rescue'},
                {'label': 'Disaster/Individual Tracking', 'value': 'Disaster Rescue'},
                {'label': 'Reset', 'value': 'Reset'}
            ],
            placeholder='Select Rescue Type',
            id='dropdown-filter',
            style={'color': '#2c3e50'},
            className='mb-0'
        ),
    ], 
    style={
        'color': 'white',
        'backgroundColor': '#2c3e50',
        'borderRadius': '8px'
    },
    className='p-3')
], className='mb-3 shadow-sm')
```

### Reusable Color Constants

**In dashboard.py:**

```python
# Color palette
COLORS = {
    'brand_red': '#c9341b',
    'dark_slate': '#2c3e50',
    'page_bg': '#F2E6E3',
    'card_bg': '#faf8f5',
    'text_primary': '#212529',
    'text_on_dark': '#ffffff',
}

# Font family
FONT_FAMILY = '"Ubuntu", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'

# Use in components
style_header={
    'backgroundColor': COLORS['dark_slate'],
    'color': COLORS['text_on_dark'],
    'fontFamily': FONT_FAMILY,
    'fontWeight': 'bold'
}
```
---

## Design System Maintenance

### When Adding New Components

1. **Check existing styles first** - Reuse established patterns
2. **Follow color palette** - Don't introduce new colors without justification
3. **Maintain spacing consistency** - Use Bootstrap spacing scale
4. **Test responsiveness** - Verify component at all breakpoints
5. **Update this guide** - Document new patterns for team

### Version History

- **v1.0** (December 2024) - Initial style guide creation
- Design reflects Project Two final submission

### Future Considerations

- Dark mode theme implementation
- Print stylesheet for reports
- Additional chart types (bar, line)
- Animation guidelines
- Loading states and skeletons

---

## Quick Reference

### Most Common Styles

```python
# Standard card
style={'backgroundColor': '#faf8f5'}
className='shadow-sm mb-4'

# Section header
html.H3('Section Title', className='mb-3')

# Button (if added)
dbc.Button('Action', color='primary', className='mt-3')

# Standard spacing
className='mb-3'  # After most elements
className='mb-4'  # Between sections
className='p-3'   # Card body padding
```

### Color Quick Reference

```python
bg_page = '#F2E6E3'      # Page background
bg_card = '#faf8f5'      # Card background  
bg_header = '#2c3e50'    # Headers, emphasis
accent = '#c9341b'       # Brand red accent
text = '#212529'         # Body text
```

---

*Last Updated: December 2024*  
*Maintained by: Sarah Dowd*  
*Questions? Email: sarahlynnedowd@gmail.com*
