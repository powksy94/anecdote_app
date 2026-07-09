import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Trois halos solaires qui explosent depuis le centre plein-écran.
/// Chaque [pulses[i].value] doit progresser de 0 → 1.
class UpdatePopupHalo extends StatelessWidget {
  final List<Animation<double>> pulses;

  const UpdatePopupHalo({super.key, required this.pulses});

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: Listenable.merge(pulses),
      builder: (context, _) => CustomPaint(
        painter: _SolarHaloPainter(pulses.map((a) => a.value).toList()),
        child: const SizedBox.expand(),
      ),
    );
  }
}

/// Peint un burst solaire par valeur : disque de halo + ring + 12 rayons triangulaires.
class _SolarHaloPainter extends CustomPainter {
  final List<double> values;

  const _SolarHaloPainter(this.values);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    // Rayon max = distance du centre au coin le plus éloigné
    final maxR = math.sqrt(
      (size.width / 2) * (size.width / 2) +
          (size.height / 2) * (size.height / 2),
    );

    for (final v in values) {
      if (v <= 0) continue;
      _drawBurst(canvas, center, v, maxR);
    }
  }

  void _drawBurst(Canvas canvas, Offset center, double v, double maxR) {
    final radius = maxR * v;
    final alpha = (1.0 - v).clamp(0.0, 1.0);

    // — Disque de halo central lumineux —
    final innerR = radius * 0.52;
    if (innerR > 1) {
      canvas.drawCircle(
        center,
        innerR,
        Paint()
          ..shader = RadialGradient(
            colors: [
              Colors.amber.withValues(alpha: alpha * 0.55),
              Colors.white.withValues(alpha: alpha * 0.22),
              Colors.transparent,
            ],
            stops: const [0.0, 0.28, 1.0],
          ).createShader(Rect.fromCircle(center: center, radius: innerR)),
      );
    }

    // — Ring externe —
    canvas.drawCircle(
      center,
      radius,
      Paint()
        ..color = Colors.amber.withValues(alpha: alpha * 0.90)
        ..style = PaintingStyle.stroke
        ..strokeWidth = (7.0 * (1.0 - v * 0.65)).clamp(0.5, 7.0),
    );

    // — Rayons solaires (12 triangles du centre vers le ring) —
    if (radius < 4) return;
    const nRays = 12;
    const halfAngle = 0.065; // ≈ 3.7 degrés
    final innerRayR = math.max(radius * 0.06, 2.0);
    final rayPaint = Paint()
      ..shader = RadialGradient(
        colors: [
          Colors.amber.withValues(alpha: alpha * 0.75),
          Colors.amber.withValues(alpha: alpha * 0.22),
          Colors.transparent,
        ],
        stops: const [0.0, 0.5, 1.0],
      ).createShader(Rect.fromCircle(center: center, radius: radius));

    for (int i = 0; i < nRays; i++) {
      final angle = i * (2 * math.pi / nRays);
      canvas.drawPath(
        Path()
          ..moveTo(
            center.dx + innerRayR * math.cos(angle - halfAngle),
            center.dy + innerRayR * math.sin(angle - halfAngle),
          )
          ..lineTo(
            center.dx + radius * math.cos(angle),
            center.dy + radius * math.sin(angle),
          )
          ..lineTo(
            center.dx + innerRayR * math.cos(angle + halfAngle),
            center.dy + innerRayR * math.sin(angle + halfAngle),
          )
          ..close(),
        rayPaint,
      );
    }
  }

  @override
  bool shouldRepaint(_SolarHaloPainter old) {
    if (old.values.length != values.length) return true;
    for (int i = 0; i < values.length; i++) {
      if (old.values[i] != values[i]) return true;
    }
    return false;
  }
}
