<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hala Al Rabwa Co - Letterhead</title>
    <!-- Premium Arabic & English Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-blue: #1b315e;
            --primary-orange: #e67e22;
            --accent-gray: #f8f9fa;
            --text-dark: #333;
            --text-light: #666;
        }

        @page {
            size: A4;
            margin: 0;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            font-family: 'Inter', 'Tajawal', sans-serif;
            -webkit-print-color-adjust: exact;
        }

        .page {
            width: 210mm;
            height: 297mm;
            background: white;
            position: relative;
            margin: 10mm auto;
            box-shadow: 0 0 20px rgba(0,0,0,0.15);
            overflow: hidden;
            box-sizing: border-box;
        }

        @media print {
            body { background-color: white; }
            .page { margin: 0; box-shadow: none; }
        }

        /* --- Geometric Decorations --- */
        
        /* Top Right Blue Triangle */
        .decoration-top-right {
            position: absolute;
            top: 0;
            right: 0;
            width: 80mm;
            height: 40mm;
            background-color: var(--primary-blue);
            clip-path: polygon(100% 0, 100% 100%, 40% 0);
            z-index: 1;
        }

        /* Side Accents (Left) */
        .side-accent-orange {
            position: absolute;
            top: 120mm;
            left: 0;
            width: 8mm;
            height: 25mm;
            background-color: var(--primary-orange);
            clip-path: polygon(0 0, 100% 25%, 100% 75%, 0 100%);
            z-index: 1;
        }

        .side-accent-blue {
            position: absolute;
            top: 148mm;
            left: 0;
            width: 8mm;
            height: 60mm;
            background-color: var(--primary-blue);
            clip-path: polygon(0 0, 100% 10%, 100% 90%, 0 100%);
            z-index: 1;
        }

        /* --- Header --- */
        header {
            position: relative;
            z-index: 2;
            padding-top: 15mm;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 2mm;
        }

        .logo-svg {
            width: 50mm;
            height: auto;
        }

        .header-content {
            width: 100%;
            margin-top: 10mm;
        }

        .orange-line {
            width: 90%;
            height: 1.5px;
            background-color: var(--primary-orange);
            margin: 10px auto;
        }

        .date-section {
            padding: 0 60px;
            color: var(--primary-orange);
            font-size: 14pt;
            font-weight: 500;
            display: flex;
            justify-content: flex-start;
        }

        .date-section span {
            margin: 0 10px;
        }

        /* --- Main Content Area --- */
        main {
            padding: 20mm 20mm;
            min-height: 180mm;
            position: relative;
            z-index: 2;
        }

        /* --- Footer --- */
        footer {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 35mm;
            background-color: var(--accent-gray);
            display: flex;
            align-items: center;
            padding: 0 40px;
            box-sizing: border-box;
            z-index: 5;
        }

        .footer-grid {
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr 1.2fr;
            gap: 20px;
            align-items: center;
        }

        .footer-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 10pt;
            color: var(--text-dark);
            border-left: 1px solid #ddd;
            padding-left: 15px;
            line-height: 1.4;
        }

        .footer-item:last-child {
            border-left: none;
            padding-left: 0;
            background-color: var(--primary-blue);
            color: white;
            height: 100%;
            padding: 15px 25px;
            margin-left: -40px; /* Bridge the gap to the edge */
            clip-path: polygon(15% 0, 100% 0, 100% 100%, 0% 100%);
            display: flex;
            justify-content: flex-end;
            text-align: right;
        }

        .footer-item svg {
            width: 18px;
            height: 18px;
            fill: var(--primary-orange);
            flex-shrink: 0;
        }

        .footer-item:last-child svg {
            fill: var(--primary-orange);
        }

        .address-text {
            font-family: 'Tajawal', sans-serif;
            font-weight: 500;
        }

        .phone-numbers, .email-web {
            font-family: 'Inter', sans-serif;
        }

    </style>
</head>
<body>

    <div class="page">
        <!-- Geometric Decorations -->
        <div class="decoration-top-right"></div>
        <div class="side-accent-orange"></div>
        <div class="side-accent-blue"></div>

        <header>
            <div class="logo-container">
                <!-- SVG Logo based on the image -->
                <svg viewBox="0 0 400 160" class="logo-svg" xmlns="http://www.w3.org/2000/svg">
                    <!-- HRC Text -->
                    <text x="200" y="70" text-anchor="middle" font-family="Inter, sans-serif" font-weight="900" font-size="75" fill="#1b315e">HRC</text>
                    <!-- Swoosh Arrow -->
                    <path d="M 140 85 C 160 110, 240 110, 280 85" stroke="#e67e22" stroke-width="6" fill="transparent" stroke-linecap="round"/>
                    <path d="M 270 95 L 280 85 L 265 80" stroke="#e67e22" stroke-width="6" fill="transparent" stroke-linecap="round" stroke-linejoin="round"/>
                    <!-- Company Name English -->
                    <text x="200" y="115" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="18" fill="#333">Hala Al Rabwa Co</text>
                    <!-- Company Name Arabic -->
                    <text x="200" y="145" text-anchor="middle" font-family="Tajawal, sans-serif" font-weight="800" font-size="18" fill="#333">شركة هـلا الربـوة</text>
                </svg>
            </div>

            <div class="header-content">
                <div class="orange-line"></div>
                <div class="date-section">
                    <span>Date: 20 &nbsp; / &nbsp; /</span>
                </div>
            </div>
        </header>

        <main>
            <!-- Content goes here -->
        </main>

        <footer>
            <div class="footer-grid">
                <!-- Phone -->
                <div class="footer-item">
                    <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
                    <div class="phone-numbers">
                        +964 781 8818 828<br>
                        +964 785 0550 055
                    </div>
                </div>
                <!-- Email/Web -->
                <div class="footer-item">
                    <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                    <div class="email-web">
                        Info@hala-r.com<br>
                        www.hala-r.com
                    </div>
                </div>
                <!-- Address -->
                <div class="footer-item">
                    <div class="address-text">
                        العراق - بغداد - نفق الشرطة<br>
                        بناية شارع الزويني
                    </div>
                    <svg viewBox="0 0 24 24" style="fill: #e67e22;"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                </div>
            </div>
        </footer>
    </div>

</body>
</html>