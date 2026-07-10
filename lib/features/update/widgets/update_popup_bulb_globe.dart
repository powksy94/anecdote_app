import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Dessine le globe en verre 3D avec halo interne, filament et reflets spéculaires.
void drawBulbGlobe(
  Canvas canvas,
  Offset gc,
  double gr, {
  required double flicker,
  required double light,
  required double breathe,
}) {
  final lit = (flicker * 0.6 + light * 0.9).clamp(0.0, 1.0);
  final glassColor = Color.lerp(
    const Color(0xFF88B4D2), // bleu froid (éteint)
    const Color(0xFFFFCC60), // ambré chaud (allumé)
    lit,
  )!;

  // Corps en verre — gradient radial 3D, source lumineuse en haut-gauche
  canvas.drawCircle(
    gc, gr,
    Paint()
      ..shader = RadialGradient(
        center: const Alignment(-0.35, -0.42),
        radius: 1.0,
        colors: [
          Color.lerp(Colors.white, glassColor, 0.18)!.withValues(alpha: 0.58),
          glassColor.withValues(alpha: 0.22),
          glassColor.withValues(alpha: 0.32),
        ],
        stops: const [0.0, 0.52, 1.0],
      ).createShader(Rect.fromCircle(center: gc, radius: gr)),
  );

  // Halo intérieur (élément chauffant / filament)
  final brightness = (math.sin(breathe * math.pi * 2) + 1) / 2 * 0.15
      + flicker * 0.50
      + light  * 0.50;
  if (brightness > 0.04) {
    final glowR = gr * 0.68;
    final glowC = Offset(gc.dx, gc.dy + 2);
    canvas.drawCircle(
      glowC, glowR,
      Paint()
        ..shader = RadialGradient(
          colors: [
            Colors.amber.withValues(alpha: brightness * 0.88),
            const Color(0xFFFF8800).withValues(alpha: brightness * 0.36),
            Colors.transparent,
          ],
          stops: const [0.0, 0.45, 1.0],
        ).createShader(Rect.fromCircle(center: glowC, radius: glowR)),
    );
  }
}

/// Dessine les reflets spéculaires et le contour du globe (à appeler après le filament).
void drawBulbGlobeOverlay(Canvas canvas, Offset gc, double gr) {
  // Contour verre (léger)
  canvas.drawCircle(
    gc, gr,
    Paint()
      ..color = Colors.white.withValues(alpha: 0.22)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.2,
  );

  // Reflet principal — grande zone lumineuse en haut-gauche
  final h1 = Offset(gc.dx - 10, gc.dy - 12);
  canvas.drawOval(
    Rect.fromCenter(center: h1, width: 22, height: 13),
    Paint()
      ..shader = RadialGradient(
        colors: [
          Colors.white.withValues(alpha: 0.80),
          Colors.white.withValues(alpha: 0.0),
        ],
      ).createShader(Rect.fromCenter(center: h1, width: 22, height: 13)),
  );

  // Reflet secondaire — petit, milieu-droite
  canvas.drawOval(
    Rect.fromCenter(center: Offset(gc.dx + 14, gc.dy - 7), width: 10, height: 6),
    Paint()..color = Colors.white.withValues(alpha: 0.40),
  );
}

/// Dessine le filament (mode normal ou cassé).
void drawBulbFilament(
  Canvas canvas,
  Offset gc, {
  required bool broken,
  required double flicker,
  required double light,
}) {
  final brightness = flicker * 0.6 + light * 0.85;
  final p = Paint()
    ..color = broken
        ? Colors.amber.shade300.withValues(alpha: 0.55)
        : Colors.amber.withValues(alpha: 0.38 + brightness * 0.57)
    ..style = PaintingStyle.stroke
    ..strokeWidth = 1.3
    ..strokeCap = StrokeCap.round;

  if (!broken) {
    // Fil de support gauche
    canvas.drawPath(
      Path()
        ..moveTo(gc.dx - 5, gc.dy + 14)
        ..cubicTo(gc.dx - 5, gc.dy + 4, gc.dx - 8, gc.dy - 4, gc.dx - 4, gc.dy - 9),
      p,
    );
    // Fil de support droit
    canvas.drawPath(
      Path()
        ..moveTo(gc.dx + 5, gc.dy + 14)
        ..cubicTo(gc.dx + 5, gc.dy + 4, gc.dx + 8, gc.dy - 4, gc.dx + 4, gc.dy - 9),
      p,
    );
    // Élément filament (zigzag)
    canvas.drawPath(
      Path()
        ..moveTo(gc.dx - 4, gc.dy - 9)
        ..lineTo(gc.dx - 7, gc.dy - 14)
        ..lineTo(gc.dx - 2, gc.dy - 17)
        ..lineTo(gc.dx + 2, gc.dy - 17)
        ..lineTo(gc.dx + 7, gc.dy - 14)
        ..lineTo(gc.dx + 4, gc.dy - 9),
      p,
    );
  } else {
    // Fil gauche cassé (fléchi aléatoirement)
    canvas.drawPath(
      Path()
        ..moveTo(gc.dx - 5, gc.dy + 14)
        ..cubicTo(gc.dx - 5, gc.dy + 4, gc.dx - 11, gc.dy + 1, gc.dx - 8, gc.dy - 4),
      p,
    );
    // Fil droit cassé
    canvas.drawPath(
      Path()
        ..moveTo(gc.dx + 5, gc.dy + 14)
        ..cubicTo(gc.dx + 5, gc.dy + 4, gc.dx + 12, gc.dy - 1, gc.dx + 9, gc.dy - 5),
      p,
    );
  }
}
