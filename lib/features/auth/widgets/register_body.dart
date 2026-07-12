import 'package:flutter/material.dart';
import 'register_progress_header.dart';

class RegisterBody extends StatelessWidget {
  final int currentStep;
  final int totalSteps;
  final PageController pageController;
  final VoidCallback onBack;
  final List<Widget> steps;

  const RegisterBody({
    super.key,
    required this.currentStep,
    required this.totalSteps,
    required this.pageController,
    required this.onBack,
    required this.steps,
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: [
          RegisterProgressHeader(
            currentStep: currentStep,
            totalSteps: totalSteps,
            onBack: onBack,
          ),
          const SizedBox(height: 8),
          Expanded(
            child: PageView(
              controller: pageController,
              physics: const NeverScrollableScrollPhysics(),
              children: steps,
            ),
          ),
        ],
      ),
    );
  }
}
