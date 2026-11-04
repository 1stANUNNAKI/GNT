# 🛡️ GitHub Noob Toolkit (GNT) — الدرع الوقائي والمساعد الذكي للمطورين (النسخة العربية)

<div align="center">

[![Language: English](https://img.shields.io/badge/Language-English_(Primary_README)-2563EB?style=for-the-badge)](./README.md)
[![اللغة: العربية](https://img.shields.io/badge/%D8%A7%D9%84%D9%84%D8%BA%D8%A9-%D8%A7%D9%84%D9%86%D8%B3%D8%AE%D8%A9_%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9_(Secondary)-10B981?style=for-the-badge)](./README_AR.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](./LICENSE)
[![Security Policy](https://img.shields.io/badge/Security-Policy_%26_SLA-EF4444?style=for-the-badge)](./SECURITY.md)

[![Pytest Suite](https://img.shields.io/badge/Pytest-25_Passed_(100%25)-10B981?style=for-the-badge&logo=pytest&logoColor=white)](./tests)
[![Skills Included](https://img.shields.io/badge/AI_Skills-8_Modular_Skills-6366F1?style=for-the-badge)](./skills)
[![Agents & Commands](https://img.shields.io/badge/Agents_%26_Commands-4_Agents_%2F_5_Commands-EC4899?style=for-the-badge)](./AGENTS.md)

### 🛠️ اللغات والتقنيات البرمجية المستخدمة في صناعة المشروع

![Python 3.11+](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Next.js 14](https://img.shields.io/badge/Next.js_14-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL_16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Stripe Billing](https://img.shields.io/badge/Stripe_Billing-635BFF?style=flat-square&logo=stripe&logoColor=white)
![GitHub App API](https://img.shields.io/badge/GitHub_Checks_API-181717?style=flat-square&logo=github&logoColor=white)

**المنظومة الوقائية المتكاملة، مهندس التوثيق القياسي (`git-docs-architect`)، وخادم `FastMCP` لحماية المبرمجين ومطوري الذكاء الاصطناعي (`Vibe Coders`) من تسريب المفاتيح السرية، تعارضات الفروع، ونقص الاعتماديات.**

[🇬🇧 Primary English Documentation (`README.md`)](./README.md) · [🤖 دليل الوكلاء والمهارات (`AGENTS.md`)](./AGENTS.md) · [🎯 دليل حالات الاستخدام (`USE_CASES_PLAYBOOK.md`)](./docs/use-cases/USE_CASES_PLAYBOOK.md) · [🛠️ دليل المساهمة (`CONTRIBUTING.md`)](./CONTRIBUTING.md) · [🛡️ سياسة الأمان (`SECURITY.md`)](./SECURITY.md) · [🔧 استكشاف الأخطاء (`TROUBLESHOOTING.md`)](./TROUBLESHOOTING.md)

</div>

---

## 🌟 1. ما هو مشروع `GNT` وماذا يقدم؟

يوفر **`GNT`** درعاً هندسياً متكاملاً يتضمن **8 مهارات ذكاء اصطناعي (`skills/`)، 4 وكلاء متخصصين (`agents/`)، 5 أوامر سريعة (`commands/`)، و 6 محركات بايثون أساسية (`core/`)** تعمل معاً لحمايتك وتنظيم مستودعاتك:

| المكون | العدد | الوظيفة والفائدة العملية |
| :--- | :-: | :--- |
| **مهارات الذكاء الاصطناعي (`skills/`)** | `8 مهارات` | تشمل مهارة هندسة وثائق GitHub القياسية (`git-docs-architect`)، درع منع تسريب التوكنات، حل التعارضات، وفحص الاعتماديات |
| **الوكلاء المتخصصون (`agents/`)** | `4 وكلاء` | مدقق الأمان، معالج تعارضات Git، مهندس الوثائق، وطبيب الاعتماديات |
| **الأوامر المباشرة (`commands/`)** | `5 أوامر` | `/gnt-scan`, `/gnt-docs`, `/gnt-heal`, `/gnt-deps`, `/gnt-score` |
| **محركات الحماية الأساسية (`core/`)** | `6 وحدات` | كشف الأسرار بالـ Regex والإنتروبيا ($H \ge 4.0$)، توليد الريدمي، ترجمة الفروقات، دمج الفروع، وفحص AST |
| **خادم `FastMCP` (`mcp_server/`)** | `6 أدوات` | ربط مباشر مع بيئات `Cursor` و `Claude Code` و `Windsurf` و `Antigravity` |

---

## 🚀 2. جدول التوجيه السريع حسب المهمة (بماذا تبدأ؟)

| المهمة التي تريد تنفيذها | الأمر أو المهارة | المحرك البرمجي |
| :--- | :--- | :--- |
| **فحص الكود قبل الرفع لمنع تسرب أي مفتاح سري أو ملف `.env`** | `/gnt-scan` أو [`secret-leak-shield`](./skills/secret-leak-shield/SKILL.md) | [`core/secrets.py`](./core/secrets.py) |
| **بناء وتنظيم وثائق أي مستودع بمنهجية ECC الكاملة (التبويبات الأربعة)** | `/gnt-docs` أو [`git-docs-architect`](./skills/git-docs-architect/SKILL.md) | [`skills/git-docs-architect/`](./skills/git-docs-architect/SKILL.md) |
| **حل تعارضات الدمج (`<<<<<<< HEAD`) بضغطة واحدة** | `/gnt-heal` أو [`smart-conflict-solver`](./skills/smart-conflict-solver/SKILL.md) | [`core/conflicts.py`](./core/conflicts.py) |
| **اكتشاف المكتبات المفقودة من `requirements.txt` قبل النشر** | `/gnt-deps` أو [`dep-doctor-scanner`](./skills/dep-doctor-scanner/SKILL.md) | [`core/dependencies.py`](./core/dependencies.py) |
| **توليد ملف `README.md` مبسط من 3 خطوات** | [`auto-readme-docgen`](./skills/auto-readme-docgen/SKILL.md) | [`core/docgen.py`](./core/docgen.py) |
| **تحويل فروقات الكود (`git diff`) إلى شرح بشري واضح** | [`vibelog-human-changelog`](./skills/vibelog-human-changelog/SKILL.md) | [`core/vibelog.py`](./core/vibelog.py) |
| **حساب تقييم صحة المستودع من `0` إلى `100` (`A+` إلى `F`)** | `/gnt-score` أو [`vibe-health-scorer`](./skills/vibe-health-scorer/SKILL.md) | [`core/health_score.py`](./core/health_score.py) |
| **ربط جميع أدوات GNT داخل محرر الذكاء الاصطناعي عبر MCP** | [`fastmcp-ide-bridge`](./skills/fastmcp-ide-bridge/SKILL.md) | [`mcp_server/server.py`](./mcp_server/server.py) |

---

## ⚖️ 3. الرخصة (MIT License)

هذا المشروع مرخص بموجب رخصة **MIT License** القياسية — راجع ملف [`LICENSE`](./LICENSE) للتفاصيل الكاملة.
