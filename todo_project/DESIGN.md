# Design System: TaskLog PRO
**Project ID:** 17099228744089417276

## 1. Visual Theme & Atmosphere
The brand personality is rooted in **High-trust Reliability** and **Frictionless Productivity**. The aesthetic follows a **Modern Corporate** philosophy with a strong lean toward **Minimalism**. 

The goal is to evoke a sense of **"Calm Control"** by utilizing generous whitespace and a restricted color palette, ensuring the interface never competes with the user's data. Visual competence is conveyed through structured grids and precise alignment.

## 2. Color Palette & Roles
The system uses a **"High-Signal"** approach where color is treated as a data dimension.

*   **Primary Emerald Green (#006948):** Reserved for brand presence, primary calls to action, and "Success" states.
*   **Neutral Slate (#505F76):** Used for secondary UI elements and neutral progress indicators.
*   **Canvas Gray (#F8FAFC):** The "Floor" or main background color, providing subtle contrast with white cards.
*   **Surface White (#FFFFFF):** Used for task cards, widgets, and primary content containers to create depth.
*   **Urgent Red (#BA1A1A):** Specifically for overdue tasks, alerts, and high-priority indicators.
*   **Tonal Border (#E5E7EB):** A subtle 1px stroke used to define card boundaries without heavy shadows.

## 3. Typography Rules
This system utilizes a professional sans-serif pairing:
*   **Headlines (Manrope):** Modern, geometric touch for titles. Hierarchy is established through weight (Bold) rather than excessive size.
*   **Body & UI (Inter):** The workhorse for high-density data. Maintains a **1.6x line height** to ensure readability in long task lists.
*   **Micro-copy:** Small, semi-bold caps for table headers and category tags to create a distinct visual break.

## 4. Component Stylings
*   **Buttons:** Precision-focused with an **8px radius**. Primary buttons use high-contrast Emerald Green; secondary buttons use a low-opacity version (Mint tint).
*   **Cards & Containers:** Softened with a **12px to 16px radius**. They sit on Level 1 (Bordered) and transition to Level 2 (Soft Shadow) on hover.
*   **Inputs & Forms:** Clean white background with a 1px Slate border. On focus, they gain a 2px soft Emerald outer glow.
*   **Badges/Chips:** Pill-shaped (fully rounded) to differentiate metadata from functional cards.

## 5. Layout Principles
*   **Structure:** Fixed Left Sidebar (**260px**) paired with a fluid main content area (capped at **1440px**).
*   **Rhythm:** Uses a strict **8px linear scale** for internal padding and margins.
*   **Elevation:** Avoids heavy black shadows. Uses **tonal layering** and whisper-soft diffused shadows `(0 10px 15px -3px rgba(0, 0, 0, 0.04))` to create a professional, "airy" feel.
