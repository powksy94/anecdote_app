import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'update_popup_painters.dart';

class UpdatePopupBackground extends StatelessWidget {
  final AnimationController ambientCtrl;
  final List<StarData> stars;

  const UpdatePopupBackground({
    super.key,
    required this.ambientCtrl,
    required this.stars,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned.fill(
      child: AnimatedBuilder(
        animation: ambientCtrl,
        builder: (context, _) {
          final t = ambientCtrl.value;
          return Stack(
            clipBehavior: Clip.none,
            children: [
              // Fond nuit étoilée (statique)
              const Positioned.fill(
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: [Color(0xFF0F0C29), Color(0xFF302B63), Color(0xFF1a1535)],
                      stops: [0.0, 0.55, 1.0],
                    ),
                  ),
                ),
              ),
              // Blob violet — haut droite
              Positioned(
                top: -35 + math.sin(t * 2 * math.pi) * 12,
                right: -25 + math.cos(t * 2 * math.pi) * 10,
                child: _blob(170, const Color(0xFF6D28D9), 0.28),
              ),
              // Blob bleu — bas gauche
              Positioned(
                bottom: -10 + math.cos(t * 2 * math.pi) * 14,
                left: -45 + math.sin(t * 2 * math.pi) * 10,
                child: _blob(150, const Color(0xFF1D4ED8), 0.20),
              ),
              // Blob violet — milieu droite
              Positioned(
                top: 100 + math.sin((t + 0.5) * 2 * math.pi) * 8,
                right: -60,
                child: _blob(120, const Color(0xFF7C3AED), 0.14),
              ),
              // Étoiles scintillantes
              Positioned.fill(
                child: CustomPaint(painter: StarsPainter(stars, t)),
              ),
            ],
          );
        },
      ),
    );
  }

  static Widget _blob(double size, Color color, double opacity) => Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: RadialGradient(
            colors: [color.withValues(alpha: opacity), Colors.transparent],
          ),
        ),
      );
}
