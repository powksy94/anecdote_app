import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class RegisterStepEmail extends StatelessWidget {
  final GlobalKey<FormState> formKey;
  final TextEditingController emailCtrl;
  final TextEditingController passwordCtrl;
  final TextEditingController confirmCtrl;
  final bool obscure;
  final VoidCallback onToggleObscure;
  final VoidCallback onNext;
  final VoidCallback onSignIn;

  const RegisterStepEmail({
    super.key,
    required this.formKey,
    required this.emailCtrl,
    required this.passwordCtrl,
    required this.confirmCtrl,
    required this.obscure,
    required this.onToggleObscure,
    required this.onNext,
    required this.onSignIn,
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
            Text(loc.registerTitle,
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(loc.registerStep1Subtitle,
                style: TextStyle(color: Theme.of(context).colorScheme.outline)),
            const SizedBox(height: 32),
            TextFormField(
              controller: emailCtrl,
              keyboardType: TextInputType.emailAddress,
              decoration: InputDecoration(
                labelText: loc.emailLabel,
                prefixIcon: const Icon(Icons.email_outlined),
                border: const OutlineInputBorder(),
              ),
              validator: (v) => (v == null || !v.contains('@')) ? loc.invalidEmail : null,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: passwordCtrl,
              obscureText: obscure,
              decoration: InputDecoration(
                labelText: loc.passwordLabel,
                prefixIcon: const Icon(Icons.lock_outlined),
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(obscure
                      ? Icons.visibility_outlined
                      : Icons.visibility_off_outlined),
                  onPressed: onToggleObscure,
                ),
              ),
              validator: (v) => (v == null || v.length < 12) ? loc.passwordMinLength : null,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: confirmCtrl,
              obscureText: obscure,
              decoration: InputDecoration(
                labelText: loc.confirmPasswordLabel,
                prefixIcon: const Icon(Icons.lock_outlined),
                border: const OutlineInputBorder(),
              ),
              validator: (v) => v != passwordCtrl.text ? loc.passwordsDoNotMatch : null,
            ),
            const SizedBox(height: 32),
            FilledButton(onPressed: onNext, child: Text(loc.nextButton)),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(loc.alreadyHaveAccount),
                TextButton(onPressed: onSignIn, child: Text(loc.signIn)),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
