import 'package:flutter/material.dart';

/// Trois halos concentriques qui rayonnent depuis le centre et s'estompent.
/// Chaque [pulses[i].value] doit aller de 0 → 1.
class UpdatePopupHalo extends StatelessWidget {
  final List<Animation<double>> pulses;

  const UpdatePopupHalo({super.key, required this.pulses});

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: Listenable.merge(pulses),
      builder: (context, _) => CustomPaint(
        painter: _HaloPainter(pulses.map((a) => a.value).toList()),
        child: const SizedBox.expand(),
      ),
    );
  }
}

class _HaloPainter extends CustomPainter {
  final List<double> values;
  const _HaloPainter(this.values);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    for (final t in values) {
      if (t <= 0) continue;
      final radius = 38.0 + t * 175.0;
      final alpha = (1.0 - t).clamp(0.0, 1.0);
      final strokeWidth = (5.0 - t * 4.0).clamp(0.8, 5.0);
      final color = Color.lerp(
        Colors.amber.withValues(alpha: alpha * 0.95),
        Colors.white.withValues(alpha: 0),
        t,
      )!;
      canvas.drawCircle(
        center,
        radius,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = strokeWidth
          ..color = color,
      );
    }
  }

  @override
  bool shouldRepaint(_HaloPainter old) {
    if (old.values.length != values.length) return true;
    for (int i = 0; i < values.length; i++) {
      if (old.values[i] != values[i]) return true;
    }
    return false;
  }
}
