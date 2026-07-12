import 'package:flutter/material.dart';

class SpotlightPainter extends CustomPainter {
  final Offset center;
  final double radius;

  const SpotlightPainter({required this.center, required this.radius});

  @override
  void paint(Canvas canvas, Size size) {
    final overlay = Path()
      ..addRect(Rect.fromLTWH(0, 0, size.width, size.height));
    final hole = Path()
      ..addOval(Rect.fromCircle(center: center, radius: radius));
    final path = Path.combine(PathOperation.difference, overlay, hole);
    canvas.drawPath(
      path,
      Paint()..color = Colors.black.withValues(alpha: 0.72),
    );
  }

  @override
  bool shouldRepaint(SpotlightPainter old) =>
      old.center != center || old.radius != radius;
}
