import 'dart:math' as math;
import 'package:flutter/material.dart';

typedef _ShardData = (double angle, double speed, double rotSpeed, double size);

final List<_ShardData> _bulbShards = _initShards();

List<_ShardData> _initShards() {
  final rng = math.Random(17);
  // 9 éclats répartis de -35° à +145° (principalement vers le bas et les côtés)
  return List.generate(9, (i) {
    final base = -0.60 + i * (math.pi * 1.55 / 8);
    return (
      base + (rng.nextDouble() - 0.5) * 0.35,
      0.45 + rng.nextDouble() * 0.75,
      (rng.nextDouble() - 0.5) * 14.0,
      3.5  + rng.nextDouble() * 8.0,
    );
  });
}

/// Dessine les éclats de verre en trajectoire parabolique (gravité vers le bas).
/// [burst] : 0→1 — 0 = explosion, 1 = éclats disparus.
void drawBulbShards(Canvas canvas, Offset gc, double burst) {
  for (final (angle, speed, rotSpeed, sz) in _bulbShards) {
    final t = burst;
    final dx = math.cos(angle) * speed * t * 160;
    final dy = math.sin(angle) * speed * t * 110 + t * t * 290;
    final opacity = (1.0 - t * 1.5).clamp(0.0, 1.0);

    if (opacity <= 0) continue;

    canvas.save();
    canvas.translate(gc.dx + dx, gc.dy + dy);
    canvas.rotate(rotSpeed * t);

    final shardPath = Path()
      ..moveTo(0,         -sz)
      ..lineTo( sz * 0.70,  sz * 0.40)
      ..lineTo(-sz * 0.85,  sz * 0.55)
      ..close();

    // Remplissage verre (bleu translucide)
    canvas.drawPath(
      shardPath,
      Paint()..color = const Color(0xFFD4EEF8).withValues(alpha: opacity * 0.42),
    );
    // Contour verre (reflet blanc)
    canvas.drawPath(
      shardPath,
      Paint()
        ..color = Colors.white.withValues(alpha: opacity * 0.76)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 0.9,
    );

    canvas.restore();
  }
}
