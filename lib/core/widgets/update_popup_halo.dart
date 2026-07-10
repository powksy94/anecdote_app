import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Trois halos solaires en parallaxe qui explosent depuis le centre plein-écran.
/// Chaque pulse a sa propre couleur et son décalage angulaire des rayons.
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

class _SolarHaloPainter extends CustomPainter {
  final List<double> values;

  const _SolarHaloPainter(this.values);

  // Couleur + décalage angulaire par pulse (effet parallaxe / profondeur)
  static const _pulseColors = [Colors.white, Colors.amber, Color(0xFFD4860A)];
  static const _rotOffsets  = [0.0, math.pi / 24, math.pi / 12]; // 0° / 7.5° / 15°

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final maxR = math.sqrt(
      (size.width / 2) * (size.width / 2) +
          (size.height / 2) * (size.height / 2),
    );

    for (int i = 0; i < values.length; i++) {
      final v = values[i];
      if (v <= 0) continue;
      _drawBurst(canvas, center, v, maxR,
        baseColor: _pulseColors[i % _pulseColors.length],
        rotOffset: _rotOffsets[i % _rotOffsets.length],
      );
    }
  }

  void _drawBurst(
    Canvas canvas,
    Offset center,
    double v,
    double maxR, {
    required Color baseColor,
    required double rotOffset,
  }) {
    final radius = maxR * v;
    final alpha  = (1.0 - v).clamp(0.0, 1.0);

    // — Disque de halo central lumineux —
    final innerR = radius * 0.52;
    if (innerR > 1) {
      canvas.drawCircle(
        center,
        innerR,
        Paint()
          ..shader = RadialGradient(
            colors: [
              baseColor.withValues(alpha: alpha * 0.55),
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
        ..color = baseColor.withValues(alpha: alpha * 0.90)
        ..style = PaintingStyle.stroke
        ..strokeWidth = (7.0 * (1.0 - v * 0.65)).clamp(0.5, 7.0),
    );

    // — Rayons solaires : 12 longs + 12 courts, 3 couches angulaires + décalage par pulse —
    if (radius < 4) return;

    const nRays = 12;
    // (halfAngle, alphaFactor) par couche : fond doux / faisceau / cœur lumineux
    const layers = [(0.22, 0.09), (0.11, 0.25), (0.048, 0.52)];

    for (int i = 0; i < nRays * 2; i++) {
      final angle  = i * (math.pi / nRays) + rotOffset;
      final rayR   = i.isEven ? radius : radius * 0.62;
      if (rayR < 2) continue;

      final innerRayR = math.max(rayR * 0.10, 3.0);
      final burstRect = Rect.fromCircle(center: center, radius: rayR);

      for (final (ha, aFactor) in layers) {
        canvas.drawPath(
          _rayPath(center, innerRayR, rayR, angle, ha),
          Paint()
            ..shader = RadialGradient(
              colors: [
                baseColor.withValues(alpha: alpha * aFactor),
                baseColor.withValues(alpha: alpha * aFactor * 0.35),
                Colors.transparent,
              ],
              stops: const [0.0, 0.55, 1.0],
            ).createShader(burstRect),
        );
      }
    }
  }

  Path _rayPath(Offset c, double innerR, double outerR, double angle, double ha) {
    return Path()
      ..moveTo(c.dx + innerR * math.cos(angle - ha), c.dy + innerR * math.sin(angle - ha))
      ..lineTo(c.dx + outerR * math.cos(angle),      c.dy + outerR * math.sin(angle))
      ..lineTo(c.dx + innerR * math.cos(angle + ha), c.dy + innerR * math.sin(angle + ha))
      ..close();
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
