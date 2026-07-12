import 'package:flutter/material.dart';

class OnboardingTooltip extends StatelessWidget {
  final String title;
  final String body;
  final String buttonLabel;
  final VoidCallback onNext;
  final bool arrowBelow;

  const OnboardingTooltip({
    super.key,
    required this.title,
    required this.body,
    required this.buttonLabel,
    required this.onNext,
    this.arrowBelow = false,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (!arrowBelow) _Arrow(pointDown: false),
        Container(
          margin: const EdgeInsets.symmetric(horizontal: 24),
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: theme.colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(title,
                  style: theme.textTheme.titleMedium
                      ?.copyWith(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text(body,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.onPrimaryContainer
                        .withValues(alpha: 0.8),
                  )),
              const SizedBox(height: 16),
              Align(
                alignment: Alignment.centerRight,
                child: FilledButton(
                  onPressed: onNext,
                  child: Text(buttonLabel),
                ),
              ),
            ],
          ),
        ),
        if (arrowBelow) _Arrow(pointDown: true),
      ],
    );
  }
}

class _Arrow extends StatelessWidget {
  final bool pointDown;
  const _Arrow({required this.pointDown});

  @override
  Widget build(BuildContext context) {
    final color =
        Theme.of(context).colorScheme.primaryContainer;
    return CustomPaint(
      size: const Size(24, 14),
      painter: _ArrowPainter(color: color, pointDown: pointDown),
    );
  }
}

class _ArrowPainter extends CustomPainter {
  final Color color;
  final bool pointDown;
  const _ArrowPainter({required this.color, required this.pointDown});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = color;
    final path = Path();
    if (pointDown) {
      path
        ..moveTo(0, 0)
        ..lineTo(size.width, 0)
        ..lineTo(size.width / 2, size.height)
        ..close();
    } else {
      path
        ..moveTo(size.width / 2, 0)
        ..lineTo(size.width, size.height)
        ..lineTo(0, size.height)
        ..close();
    }
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(_ArrowPainter old) =>
      old.color != color || old.pointDown != pointDown;
}
