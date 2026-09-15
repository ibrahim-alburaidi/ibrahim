# بديل | Badil

**مساعد ذكي لتسليم واستلام العمل**

ملف أعمال تدريبي باللغة العربية يوضح استخدام الذكاء الاصطناعي التوليدي لتحويل الرسائل وملاحظات العمل إلى تسليم منظم، مع ربط المهام بمصادرها، وكشف النواقص واختلافات المواعيد، وإبقاء الاعتماد النهائي للإنسان.

| Item | Details |
|---|---|
| **Project Name** | **Badil — بديل** |
| **Course Name** | Generative AI for Workplace Productivity |
| **Course Code** | L0-FGP |
| **Training Academy** | [@SDAIAAcademy](https://github.com/SDAIAAcademy) |
| **Instructor** | Fahad Alqahtani |
| **Trainee** | **ibrahim abdullah alburaidi** |
| **Professional Scenario** | Operations Coordinator — Employee Handover and Work Continuity |
| **Submission Date** | 15 September 2026 |

**المتدرب:** إبراهيم البريدي. **المدرب:** فهد القحطاني. **الإصدار:** v0.1.2 — نسخة النشر بموافقة المتدرب.

السيناريو المهني: منسق عمليات يجهز تسليم العمل ويحافظ على استمراريته أثناء غياب الموظف. هذا ملف أعمال توثيقي وأوامر قابلة للتجربة. [بيانات التدريب](docs/training-program.md).

## المشكلة والقيمة

عند غياب الموظف قد تتوزع مسؤولياته بين رسائل ومحاضر وجداول، فيصعب على البديل معرفة المطلوب ومواعيده والعوائق. ينظم «بديل» هذه المعلومات في ملف متابعة واحد، ويكشف ما ينقص قبل التسليم بدل ملء الفراغات بافتراضات.

نقطة التميز: **كل مهمة لها مصدر، وكل نقص أو اختلاف ظاهر وقابل للمتابعة.** ولا يعني تعيين البديل أنه أصبح مالكًا لكل مهمة لدى الأقسام الأخرى.

## تجربة سريعة

لا تحتاج القراءة إلى تثبيت برامج أو مفاتيح API:

1. اقرأ [السيناريو](examples/scenario.md) و[الرسائل والمحضر](examples/raw-input.md).
2. افتح [ملف التسليم المرجعي](outputs/handover.md)، ثم [الأسئلة المفتوحة](outputs/open-questions.md).
3. لتجربة AI بنفسك، انسخ P01 من [مكتبة الأوامر](01-prompt-engineering/prompt-library.md) وأرفق المدخلات الافتراضية كاملة في أداة محادثة مناسبة.
4. طبق P02 وP03 لكشف الاختلافات والنواقص، ثم P06 للتحقق.
5. قارن الناتج بالمرجع، وسجل الفروق ومراجعتك في [سجل المراجعة](05-verification/review-log.md). قد تختلف صياغة الناتج من تشغيل لآخر.
6. استخدم P04 وP05 لإعداد رسالة وخطة، واعتمدهما بشريًا قبل الاستخدام. دليل أوسع في [دليل الاستخدام](docs/user-guide.md).

## مثال على النتيجة

| المعلومة الواردة | معالجة بديل |
|---|---|
| الفاتورة لدى المالية دون تأكيد صرف | الصرف غير مؤكد؛ مسؤول الاستفسار غير محدد |
| المورد يسجل 6 أكتوبر والعمليات تسجل 7 أكتوبر | اختلاف موعد يحتاج حسمًا؛ لا نختار الأحدث تلقائيًا |
| سارة بديلة والصلاحية لم تفعل | عائق تشغيل يحتاج مسؤول تنفيذ ودليل تفعيل |
| التقرير ينتظر بيانات نور | إبقاء يوسف مسؤولًا، وإظهار الاعتماد على البيانات |

هذه أمثلة مرجعية أُنشئت لهذا المشروع، وليست سجل نتائج تشغيل خارجي. [المصادر](examples/raw-input.md).

## الأقسام السبعة

| القسم | المحتوى |
|---|---|
| [01 — هندسة الأوامر](01-prompt-engineering/prompt-library.md) | 7 أوامر C.A.R.E./R.C.T.O. ومثال [قبل/بعد](01-prompt-engineering/before-after-example.md) |
| [02 — الكتابة المهنية](02-writing-workflow/professional-writing-example.md) | Draft → Verify → Refine → Human Sign-off، مع أخطاء تعليمية وتصحيحها |
| [03 — معالجة المعلومات](03-information-workflow/information-processing-example.md) | تلخيص واستخراج وإعادة هيكلة وترتيب أولويات |
| [04 — التخطيط](04-planning-workflow/planning-example.md) | Goal → Mechanisms → Phases → Tasks واعتماديات وقرارات بشرية |
| [05 — التحقق](05-verification/verification-checklist.md) | Identify → Set Criteria → Test → Confirm and Decide، وقائمة وسجل مراجعة |
| [06 — الاستخدام المسؤول](06-responsible-ai/responsible-use-checklist.md) | المبادئ الستة وتصنيف Green / Amber / Red |
| [07 — خطة الدمج](07-integration-plan/personal-integration-plan.md) | خطة 30 يومًا ومقاييس نجاح لا تفترض نتائج مسبقة |

## الملفات المساندة

| المسار | الغرض |
|---|---|
| [examples/](examples/) | 15 رسالة ومحضر واحد ببيانات افتراضية، ونسخة JSON |
| [outputs/](outputs/) | 8 مهام، ملف تسليم، أسئلة استكمال، وخطة متابعة |
| [docs/technical-documentation.md](docs/technical-documentation.md) | تصميم سير العمل، مخطط البيانات، قواعد المعالجة وحدودها |
| [docs/requirements-mapping.md](docs/requirements-mapping.md) | مطابقة متطلبات التسليم مع ملفات المشروع |
| [docs/git-workflow.md](docs/git-workflow.md) | سير Git المطبق وخطوات التطوير والنشر |
| [docs/demo-guide.md](docs/demo-guide.md) | سيناريو عرض قصير للمشروع |
| [evaluation/measurement-template.md](evaluation/measurement-template.md) | قالب لتوثيق تجربة فعلية وقياس الزمن والدقة |
| [scripts/validate_project.py](scripts/validate_project.py) | فحص محلي للبنية والمراجع والحقائق الحرجة |
| [evaluation/revision-audit.md](evaluation/revision-audit.md) | نتائج التدقيق الثاني والأخطاء التي عولجت |
| [outputs/evidence-map.md](outputs/evidence-map.md) | دليل المسؤول والموعد والحالة لكل مهمة |
| [CHANGELOG.md](CHANGELOG.md) | سجل تغييرات الإصدار |
| [CONTRIBUTING.md](CONTRIBUTING.md) | قواعد المساهمة والتعديل |

## الفحص التقني الاختياري

يتطلب Python 3.10 أو أحدث، ويستخدم المكتبة القياسية فقط. من داخل مجلد المشروع:

```bash
python scripts/validate_project.py
```

على الأنظمة التي تسمي الأمر `python3` استخدمه بدلًا من `python`. يعرض الفحص PASS عند النجاح ويعيد رمز خروج غير صفري عند الإخفاق. هو فحص للمستندات والبيانات المرجعية، **ولا يشغّل نموذج ذكاء اصطناعي** ولا يغني عن مراجعة الإنسان.

لإعادة تشغيل اختبارات الفاحص: `python scripts/test_validation.py`. تفاصيل ما فُحص وما صُحح في [تقرير التدقيق](evaluation/revision-audit.md).

## إدارة الإصدارات

المستودع: [ibrahim-alburaidi/ibrahim](https://github.com/ibrahim-alburaidi/ibrahim). يتضمن النشر commits متتابعة وواضحة، مع حفظ تاريخ الإعداد المحلي ووسمي v0.1.0 وv0.1.1 داخل [Git bundle](history/badil-history.bundle). يختلف تاريخ الرفع عن تاريخ الإعداد؛ لا توجد Pull Request أو GitHub Release منشأة. [تفاصيل الإصدارات](docs/git-workflow.md).

## القيود والمراجعة

لا توجد تكاملات بريد أو لوحة تشغيل أو إرسال تلقائي؛ التنفيذ هنا سير عمل تدريبي موثق مثل المثالين المرجعيين. لا توجد نتائج توفير زمن مقاسة أو موافقة متدرب مسجلة. كل البيانات التشغيلية افتراضية، والمسودات المعلمة بالأخطاء صُممت لتمارين المراجعة.

## البرنامج والمراجع

أُعد هذا المشروع ضمن برنامج **Generative AI for Workplace Productivity** بأكاديمية سدايا، بإشراف المدرب **Fahad Alqahtani**، باسم المتدرب **ibrahim abdullah alburaidi** وفق البيانات التي قدمها. رمز الدورة **L0-FGP**  لا يمثل شهادة أو نتيجة تقييم. 

حساب الأكاديمية الرسمي المطلوب ضمن المشروع: **[SDAIAAcademy](https://github.com/SDAIAAcademy)**.
