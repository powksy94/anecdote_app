import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class RegisterStepName extends StatelessWidget {
  final GlobalKey<FormState> formKey;
  final TextEditingController nameCtrl;
  final VoidCallback onNext;

  const RegisterStepName({
    super.key,
    required this.formKey,
    required this.nameCtrl,
    required this.onNext,
  });

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(loc.registerStep2Title,
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(loc.registerStep2Subtitle,
                style: TextStyle(color: Theme.of(context).colorScheme.outline)),
            const SizedBox(height: 32),
            TextFormField(
              controller: nameCtrl,
              textCapitalization: TextCapitalization.words,
              decoration: InputDecoration(
                labelText: loc.firstNameLabel,
                prefixIcon: const Icon(Icons.person_outlined),
                border: const OutlineInputBorder(),
              ),
              validator: (v) =>
                  (v == null || v.trim().isEmpty) ? loc.requiredField : null,
            ),
            const SizedBox(height: 32),
            FilledButton(onPressed: onNext, child: Text(loc.nextButton)),
          ],
        ),
      ),
    );
  }
}
