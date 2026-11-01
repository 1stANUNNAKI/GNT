# 🛡️ نموذج الأمان وحماية الأسرار · Security Model

> **السياسة الأمنية:** انعدام الثقة المطلق (Zero Trust Architecture)  
> **الاعتماد:** التدقيق الأمني الصارم ومكافحة تسريب البيانات الحساسة

---

## 1. نموذج كشف الأسرار (Secret Leak Shield Engine)
يعمل درع الأسرار على مستويين رئيسيين:

### المستوى الأول: مطابقة الأنماط الحتمية (Deterministic Regex Signatures)
يغطي الدرع مفاتيح الخدمات السحابية والذكاء الاصطناعي ومزودي الدفع:
1. **OpenAI API Keys:** `sk-[A-Za-z0-9]{48}`, `sk-proj-[A-Za-z0-9_\-]{48,}`
2. **Anthropic Claude Keys:** `sk-ant-[A-Za-z0-9_\-]{32,}`
3. **Stripe Secret Keys:** `sk_live_[0-9a-zA-Z]{24,}`, `rk_live_[0-9a-zA-Z]{24,}`
4. **AWS Access Key ID & Secret:** `AKIA[0-9A-Z]{16}`, `aws_secret_access_key`
5. **GitHub Personal Access Tokens:** `ghp_[0-9a-zA-Z]{36}`, `github_pat_[0-9a-zA-Z_]{82}`
6. **SSH / RSA Private Keys:** `-----BEGIN ((EC|RSA|DSA|OPENSSH) )?PRIVATE KEY-----`
7. **Slack Bot / User Tokens:** `xox[baprs]-[0-9a-zA-Z]{10,}`
8. **Generic High-Security Tokens:** رموز مفاتيح بصيغ Hex أو Base64 مسبوقة بكلمات `api_key`, `token`, `secret`.

### المستوى الثاني: حساب مقياس الإنتروبيا (Shannon Entropy Calculation)
يتم احتساب كثافة العشوائية لأي سلسلة نصية مريبة تزيد عن 20 حرفاً. إذا تجاوزت الإنتروبيا عتبة `4.5` وكانت مصحوبة بمتغيرات تعيين في الكود، يتم تصنيفها كاشتباه عالي الخطورة.

---

## 2. إدارة وتأمين الويب هوك (Webhook Security)
- كل طلب وارد من جيت هاب يخضع لحساب HMAC SHA-256 باستخدام `WEBHOOK_SECRET` السري المحفوظ في المتغيرات البيئية.
- في حال عدم تطابق التوقيع `X-Hub-Signature-256` أو غيابه، يتم رفض الطلب فوراً بكود `401 Unauthorized` قبل معالجة أي محتوى.
- منع هجمات إعادة الإرسال (Replay Attacks) عبر التحقق من طابع الوقت الزمني للحدث.

---

## 3. تأمين خادم MCP وواجهات الـ REST
- مصادقة خادم MCP عبر Bearer API Tokens المشفرة بـ SHA-256.
- حماية واجهات REST الخاصة بـ SaaS بواسطة JWT قصيرة الصلاحية (Access Token: 15 دقيقة، Refresh Token: 7 أيام مع HttpOnly Cookie).
- تقييد معدل الطلبات (Rate Limiting) على مستوى الـ IP وحساب المستخدم لمنع الاستنزاف والحرمان من الخدمة (DDoS Mitigation).
