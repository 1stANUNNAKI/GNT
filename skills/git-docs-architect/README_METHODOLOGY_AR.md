# 🏛️ الدليل الهندسي الشامل لمنهجية توثيق وهيكلة مستودعات GitHub (منهجية ECC & GNT)

> **المسار المرجعي:** `D:\bulid git docs`  
> **المهارة البرمجية:** [`SKILL.md`](./SKILL.md) (`git-docs-architect`)  
> **النموذج المرجعي المحلل:** [`1stANUNNAKI/ECC-FORK`](https://github.com/1stANUNNAKI/ECC-FORK) و [`1stANUNNAKI/GNT`](https://github.com/1stANUNNAKI/GNT)

---

## 🔍 أولاً: تحليل تشريحي كامل لوثائق مستودع `ECC-FORK` وكيف تعمل تبويبات GitHub العلوية

عندما تفتح مستودع [`1stANUNNAKI/ECC-FORK`](https://github.com/1stANUNNAKI/ECC-FORK?tab=security-ov-file) على GitHub، تلاحظ ظهور شريط تبويبات احترافي أعلى ملفات الكود يحتوي على:
1. **`📖 Readme`**
2. **`🤝 Code of conduct`**
3. **`⚖️ MIT license`**
4. **`🛡️ Security`**

هذه التبويبات لا تُضاف بزر يدوي في إعدادات الموقع، بل يقوم **محرك صحة المجتمع في كيتهاب (GitHub Community Health & Licensee Engine)** بقراءة جذر المستودع تلقائياً، وبمجرد عثوره على الملفات القياسية بالأسماء والهيكل الصحيح، يُفعّل هذه التبويبات فوراً ويرفع تقييم المستودع (`Community Standards`) إلى **100%**.

فيما يلي تشريح دقيق لكل ملف من هذه الملفات وكيف تم إعداده فقرةً بفقرة:

---

### 1. 📄 تشريح ملف `README.md` (الواجهة الهندسية والتسويقية للمشروع)
في منهجية `ECC`، لا يُكتب ملف `README.md` كنص عشوائي، بل يُبنى من **10 طبقات متسلسلة (10 Architectural Zones)**:

1. **الطبقة 1 — الهوية البصرية، مبدل اللغات، وشارات الثقة (Header & Language Bar):**
   - شريط تبديل اللغات في الأعلى (`English (Primary)` | `العربية (README_AR.md)`).
   - شارات الحالة الرسمية (`Tests Passed`, `License: MIT`, `Security Policy`, `MCP Ready`).
   - **شريط اللغات والتقنيات (`Built With`):** شارات ملونة لكل لغة وإطار عمل مستخدم في بناء المشروع (`Python`, `TypeScript`, `Next.js`, `FastAPI`, `Docker`, `PostgreSQL`).
2. **الطبقة 2 — تنبيه المصادر الرسمية وحدود الثقة (`> [!WARNING] Official Sources Only`):**
   - صندوق تحذيري بارز يحدد الروابط والحزم الرسمية المعتمدة للمشروع لحماية المستخدمين من النسخ المقلدة أو هجمات سلسلة التوريد (`Supply-Chain Attacks`).
3. **الطبقة 3 — معادلة القيمة وخط سير العمل (`Value Pipeline & Summary Table`):**
   - سطر برمجي يلخص دورة حياة العمل، مثل:
     `scan -> detect -> heal -> document -> verify -> deploy`
   - يتبعه **جدول إحصائي سريع (`Included | Count | What it gives you`)** يوضح بالأرقام عدد المهارات (`Skills`)، الوكلاء (`Agents`)، الأوامر (`Commands`)، والوحدات الأساسية (`Core Modules`).
4. **الطبقة 4 — المخطط المعماري التفاعلي (`Mermaid Architecture Diagram`):**
   - مخطط `Mermaid` يوضح تدفق البيانات بين واجهة المطور (`AI IDE / CLI / GitHub Webhook`) ومحرك المعالجة (`Core Engine`) وقاعدة البيانات.
5. **الطبقة 5 — دليل التثبيت الموجه متعدد البيئات (`Guided Setup & Multi-Harness Install`):**
   - أوامر تثبيت جاهزة للنسخ واللصق عبر مختلف مدراء الحزم (`pnpm`, `npm`, `pip`, `uv`, `docker compose`).
   - استخدام القوائم المطوية `<details><summary>...</summary></details>` لإخفاء الإعدادات المتقدمة حتى تظل الصفحة الرئيسية نظيفة وسريعة القراءة.
6. **الطبقة 6 — جدول التوجيه حسب المهمة (`Start Using — Task-to-Skill Router`):**
   - بدلاً من إجبار الزائر على قراءة كل الكود، يقدّم جدولاً عملياً: **"ماذا تريد أن تفعل؟ (`What you are doing`) ← ابدأ من هنا (`Start here`) ← المهارة أو الوكيل المستخدم (`Skill / Agent`)"**.
7. **الطبقة 7 — شجرة المكونات المشروحة (`What's Inside — Annotated Component Tree`):**
   - شجرة مجلدات ASCII توضح وظيفة كل مجلد وملف رئيسي في المستودع.
8. **الطبقة 8 — بوابة التحقق التشغيلي (`Operational Verification — verify: PASS`):**
   - أمر تشغيل الاختبارات الفعلي (`pytest -v`) مع نتيجة النجاح الموثقة لإثبات موثوقية الكود.

---

### 2. 🤝 تشريح ملف `CODE_OF_CONDUCT.md` (ميثاق السلوك المهني)
يتبع المعيار العالمي **Contributor Covenant v2.0** مع **سلم الإنفاذ الرباعي لمؤسسة Mozilla**، ويتكون من **7 فقرات أساسية**:
1. **`## Our Pledge` (تعهدنا):** التزام قادة المشروع والمساهمين بتوفير بيئة عمل احترافية خالية من المضايقات للجميع.
2. **`## Our Standards` (معاييرنا):**
   - أمثلة السلوك الإيجابي (التعاطف، قبول النقد البناء، تحمل المسؤولية).
   - أمثلة السلوك المرفوض (الهجمات الشخصية، نشر بيانات أو توكنات خاصة بالآخرين دون إذن).
3. **`## Enforcement Responsibilities` (مسؤوليات الإنفاذ):** حق مشرفي المستودع في تعديل أو رفض أي تعليق أو `Commit` أو `PR` يخالف المعايير.
4. **`## Scope` (نطاق التطبيق):** يسري الميثاق داخل جميع مساحات المستودع (`Issues`, `PRs`, `Discussions`).
5. **`## Enforcement` (آلية الإبلاغ):** قناة التواصل للإبلاغ عن المخالفات مع ضمان سرية المبلّغ.
6. **`## Enforcement Guidelines` (سلم العقوبات التدريجي من 4 مستويات):**
   - **المستوى 1 (`1. Correction`):** تنبيه خاص مكتوب لتوضيح الخطأ غير المقصود.
   - **المستوى 2 (`2. Warning`):** إنذار رسمي عند تكرار المخالفة مع منع التفاعل المؤقت.
   - **المستوى 3 (`3. Temporary Ban`):** حظر مؤقت من المشاركة في المستودع لفترة محددة.
   - **المستوى 4 (`4. Permanent Ban`):** حظر دائم في حال المخالفات الجسيمة أو المتكررة.
7. **`## Attribution` (الإسناد القانوني):** الإشارة إلى رخصة ومصدر `Contributor Covenant v2.0`.

---

### 3. 🛡️ تشريح ملف `SECURITY.md` (سياسة الأمان وحماية سلسلة التوريد)
هذا الملف هو الذي يفتح تبويب **`Security`** في أعلى المستودع (`?tab=security-ov-file`). في منهجية `ECC`، يُصمم كوثيقة أمنية تشغيلية من **8 أقسام**:
1. **`## Supported Versions` (الإصدارات المدعومة):** جدول يوضح أي إصدارات تستقبل تحديثات أمنية فورية (`:white_check_mark:`).
2. **`## Reporting a Vulnerability` (الإبلاغ السري عن الثغرات):**
   - رابط مباشر لميزة **GitHub Private Vulnerability Reporting** (`/security/advisories/new`).
   - تحذير صريح بعدم فتح `Public Issue` للثغرات الأمنية.
   - تحديد ما يجب إرفاقه في التقرير (المسار، خطوات إعادة الإنتاج، حدود الثقة المخترقة).
   - **اتفاقية مستوى الاستجابة (`Response SLA`):** تأكيد الاستلام خلال **48 ساعة**، التقييم الأولي خلال **7 أيام**، وإصلاح الثغرات الحرجة خلال **14 يوماً**.
3. **`## Scope` (النطاق الأمني):** تحديد المكونات المشمولة (الخلفية، الـ API، خادم الـ MCP، تطبيق GitHub، وسير عمل GitHub Actions).
4. **`## Official Distribution Surfaces` (قنوات التوزيع الرسمية):** تحديد المستودع الرسمي والحزم المعتمدة لمنع انتحال الهوية.
5. **`## Out of Scope` (خارج النطاق):** توضيح الحالات التي لا تُعد ثغرة في المشروع (مثل تشغيل المستخدم لأوامر محلية بيده دون عبور حدود ثقة).
6. **`## Supply-Chain Rules` (قواعد سلسلة التوريد):** تثبيت إصدارات GitHub Actions، ومنع تمرير مدخلات غير موثوقة مباشرة إلى أوامر الشل.
7. **`## Operational Guidance — Secrets Handling` (الدليل التشغيلي لحماية الأسرار):**
   - منع كتابة أي مفاتيح حقيقية في `.env` أو `mcp.json`.
   - توفير أوامر فحص جاهزة بـ `grep` (لـ Linux/macOS) و `Select-String` (لـ Windows PowerShell) ليكتشف المطور فوراً أي توكن مسرب في جهازه.
8. **`## Security Resources` (المراجع الأمنية):** روابط `OWASP MCP Top 10` و `OWASP Top 10 for Agentic Applications`.

---

### 4. 🛠️ تشريح ملف `CONTRIBUTING.md` (دليل المساهمة الهندسي)
يظهر رابطه تلقائياً لأي مطور يفتح `Pull Request` أو `Issue` جديد، ويتكون من:
1. **`## What We're Looking For`:** تحديد أنواع المساهمات المطلوبة (`Skills`, `Agents`, `Core Modules`, `MCP Tools`, `Tests`).
2. **`## Quick Start`:** خطوات الـ 5 دقائق (`Fork` ← `Branch` ← `Code` ← `Test` ← `PR`).
3. **`## Contributing Skills (`skills/<name>/SKILL.md`)`:**
   - القالب القياسي لملف `SKILL.md` (ترويسة YAML Frontmatter + متى تُفعّل المهارة + المفاهيم + أمثلة الكود + الأنماط الخاطئة `Anti-Patterns` + قائمة التحقق من 11 بنداً).
4. **`## Contributing Agents & Commands`:** القالب القياسي للوكلاء (`agents/*.md`) والأوامر (`commands/*.md`).
5. **`## Pull Request Process & Pre-Push Gauntlet`:**
   - صيغة عناوين طلبات السحب (`feat(skills): ...`, `fix(core): ...`).
   - قائمة الفحص الإلزامية قبل الرفع (`pytest -v` وفحص خلو التوكنات).

---

### 5. ⚖️ تشريح ملف `LICENSE` وملفات المساندة (`AGENTS.md`, `CHANGELOG.md`, `TROUBLESHOOTING.md`)
- **`LICENSE`:** نص رخصة **MIT License** القياسي الذي يفعل تبويب `⚖️ MIT license`.
- **`AGENTS.md`:** دستور عمل وكلاء الذكاء الاصطناعي داخل المستودع (المبادئ الخمسة، جدول الوكلاء والمهارات، قائمة فحص الأمان قبل أي Commit، ومعيار تغطية الاختبارات 80%+).
- **`CHANGELOG.md`:** سجل الإصدارات الزمني المصنف (`Added`, `Changed`, `Fixed`, `Security`).
- **`TROUBLESHOOTING.md`:** دليل تشخيص وإصلاح الأعطال الشائعة (`Symptom` ← `Causes` ← `Solutions`).

---

## 🚀 ثانياً: كيف تستخدم هذه المهارة (`D:\bulid git docs`) على أي مشروع؟

يحتوي هذا المجلد (`D:\bulid git docs`) على:
1. [`SKILL.md`](./SKILL.md): ملف المهارة الجاهز للوكلاء (`git-docs-architect`).
2. [`templates/`](./templates/): القوالب القياسية الكاملة لجميع الملفات التسعة.
3. [`scripts/build_git_docs.py`](./scripts/build_git_docs.py): أداة سطر الأوامر الآلية لتوليد وفحص حزمة التوثيق الكاملة لأي مشروع:

```bash
python "D:\bulid git docs\scripts\build_git_docs.py" --repo-dir ./path/to/repo --project-name "MY-PROJECT" --owner "1stANUNNAKI"
```
