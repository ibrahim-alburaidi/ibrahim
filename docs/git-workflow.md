# إدارة الإصدارات

## المستودع المنشور

المشروع «بديل» في مستودع [ibrahim-alburaidi/ibrahim](https://github.com/ibrahim-alburaidi/ibrahim)، الذي كان فارغًا قبل رفع المشروع. وافق إبراهيم على النشر صراحة في 2026-09-15.

الإصدار الموثق الحالي v0.1.2. سجل الرفع يتكون من commits متتابعة: تهيئة المستودع، إضافة بيانات السيناريو ومخرجاته، ثم استكمال الأقسام والتوثيق والفحص. لم تُنشأ GitHub Release أو وسوم بعيدة ضمن النشر الأولي.

## تاريخ الإعداد السابق

حُفظ تاريخ الإعداد المحلي الكامل حتى v0.1.1، بما فيه الفروع والدمج ووسما v0.1.0 وv0.1.1، في [badil-history.bundle](../history/badil-history.bundle). هذا تاريخ مستقل عن commits الرفع؛ لم يُعد تمثيله باعتباره سجل GitHub الأصلي.

لاستعادة تاريخ الإعداد القديم، حمّل ملف bundle ثم نفذ:

```bash
git clone badil-history.bundle badil-original-history
```

هذه نسخة تاريخية. للعمل على المشروع الحالي استخدم clone من GitHub:

```bash
git clone https://github.com/ibrahim-alburaidi/ibrahim.git
cd ibrahim
python scripts/validate_project.py
python scripts/test_validation.py
```

## دورة التعديل

```bash
git switch -c docs/improve-handover
```

عدّل الملفات المحددة، وأضف مصادر لأي تغيير في الحقائق. شغّل الفحص وراجع المعنى، ثم أضف الملفات التي عدلتها فقط وأنشئ commit برسالة واضحة، مثل `docs: clarify handover evidence`. ارفع فرعك وافتح Pull Request باستخدام [القالب](../.github/pull_request_template.md).

استخدم `docs:` للتوثيق و`fix:` للتصحيح و`feat:` للإضافات. اضبط اسم وبريد Git الخاصين بك عند مساهمتك، ولا تضع رموز وصول في الملفات. حدّث CHANGELOG عند الإصدار التالي ولا تستخدم force push لتعديل عادي. وسوم الإعداد داخل bundle لا تظهر تلقائيًا في صفحة وسوم GitHub.
