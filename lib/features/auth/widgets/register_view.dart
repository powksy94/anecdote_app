import 'package:flutter/material.dart';
import 'register_body.dart';

class RegisterView extends StatelessWidget {
  final int step;
  final int totalSteps;
  final PageController pageCtrl;
  final VoidCallback onBack;
  final Widget stepEmail;
  final Widget stepName;
  final Widget stepCategories;

  const RegisterView({
    super.key,
    required this.step,
    required this.totalSteps,
    required this.pageCtrl,
    required this.onBack,
    required this.stepEmail,
    required this.stepName,
    required this.stepCategories,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RegisterBody(
        currentStep: step,
        totalSteps: totalSteps,
        pageController: pageCtrl,
        onBack: onBack,
        steps: [stepEmail, stepName, stepCategories],
      ),
    );
  }
}
