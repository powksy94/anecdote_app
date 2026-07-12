import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../models/onboarding_step.dart';
import '../painters/spotlight_painter.dart';
import 'onboarding_tooltip.dart';

class OnboardingOverlay extends StatefulWidget {
  final VoidCallback onDone;
  const OnboardingOverlay({super.key, required this.onDone});

  @override
  State<OnboardingOverlay> createState() => _OnboardingOverlayState();
}

class _OnboardingOverlayState extends State<OnboardingOverlay> {
  int _stepIndex = 0;

  List<OnboardingStep> _buildSteps(AppLocalizations loc) => [
        OnboardingStep(
          anchor: SpotlightAnchor.favoritesTab,
          title: loc.onboardingOverlayFavoritesTitle,
          body: loc.onboardingOverlayFavoritesBody,
          spotlightRadius: 44,
        ),
        OnboardingStep(
          anchor: SpotlightAnchor.accountIcon,
          title: loc.onboardingOverlayAccountTitle,
          body: loc.onboardingOverlayAccountBody,
          spotlightRadius: 32,
        ),
        OnboardingStep(
          anchor: SpotlightAnchor.none,
          title: loc.onboardingOverlayDoneTitle,
          body: loc.onboardingOverlayDoneBody,
          isLast: true,
        ),
      ];

  void _next(List<OnboardingStep> steps) {
    if (_stepIndex < steps.length - 1) {
      setState(() => _stepIndex++);
    } else {
      widget.onDone();
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final steps = _buildSteps(loc);
    final step = steps[_stepIndex];
    final size = MediaQuery.of(context).size;
    final padding = MediaQuery.of(context).padding;
    final center = step.resolveCenter(size, padding);

    return GestureDetector(
      onTap: () {}, // absorb taps on the dark overlay
      child: SizedBox.expand(
        child: Stack(
          children: [
            IgnorePointer(
              child: CustomPaint(
                size: size,
                painter: SpotlightPainter(
                  center: center,
                  radius: step.anchor == SpotlightAnchor.none
                      ? 0
                      : step.spotlightRadius,
                ),
              ),
            ),
            _positionedTooltip(context, step, center, size, padding, steps, loc),
          ],
        ),
      ),
    );
  }

  Widget _positionedTooltip(
    BuildContext context,
    OnboardingStep step,
    Offset center,
    Size size,
    EdgeInsets padding,
    List<OnboardingStep> steps,
    AppLocalizations loc,
  ) {
    final tooltip = OnboardingTooltip(
      title: step.title,
      body: step.body,
      buttonLabel: step.isLast ? loc.onboardingOverlayGotIt : loc.nextButton,
      onNext: () => _next(steps),
      arrowBelow: step.tooltipAbove,
    );

    if (step.anchor == SpotlightAnchor.none) {
      return Center(child: tooltip);
    }

    if (step.tooltipAbove) {
      // Tooltip above spotlight (e.g. favorites tab at bottom)
      return Positioned(
        bottom: size.height - center.dy + step.spotlightRadius + 8,
        left: 0,
        right: 0,
        child: tooltip,
      );
    } else {
      // Tooltip below spotlight (e.g. account icon at top)
      return Positioned(
        top: center.dy + step.spotlightRadius + 8,
        left: 0,
        right: 0,
        child: tooltip,
      );
    }
  }
}
