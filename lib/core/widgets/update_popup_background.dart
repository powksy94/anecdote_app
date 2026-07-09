import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'update_popup_painters.dart';

class UpdatePopupBackground extends StatelessWidget {
  final AnimationController ambientCtrl;
  final List<StarData> stars;

  /// Quand [dimmingAnim] est non-null, un brouillard sombre descend
  /// progressivement sur le fond (value : 0 → clair, 1 → quasi-noir).
  final Animation<double>? dimmingAnim;

  const UpdatePopupBackground({
    super.key,
    required this.ambientCtrl,
    required this.stars,
    this.dimmingAnim,
  });

  @override
  Widget build(BuildContext context) {
    final listenables = <Listenable>[ambientCtrl];
    if (dimmingAnim != null) listenables.add(dimmingAnim!);

    return Positioned.fill(
      child: AnimatedBuilder(
        animation: Listenable.merge(listenables),
        builder: (context, _) {
          final t = ambientCtrl.value;
          final dim = dimmingAnim?.value ?? 0.0;

          return Stack(
            clipBehavior: Clip.none,
            children: [
              // Fond nuit étoilée
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
                child: _blob(170, const Color(0xFF6D28D9), 0.28 * (1 - dim)),
              ),
              // Blob bleu — bas gauche
              Positioned(
                bottom: -10 + math.cos(t * 2 * math.pi) * 14,
                left: -45 + math.sin(t * 2 * math.pi) * 10,
                child: _blob(150, const Color(0xFF1D4ED8), 0.20 * (1 - dim)),
              ),
              // Blob violet — milieu droite
              Positioned(
                top: 100 + math.sin((t + 0.5) * 2 * math.pi) * 8,
                right: -60,
                child: _blob(120, const Color(0xFF7C3AED), 0.14 * (1 - dim)),
              ),
              // Étoiles scintillantes
              Positioned.fill(
                child: Opacity(
                  opacity: (1 - dim).clamp(0.0, 1.0),
                  child: CustomPaint(painter: StarsPainter(stars, t)),
                ),
              ),
              // — Brouillard sombre —
              if (dim > 0)
                Positioned.fill(
                  child: DecoratedBox(
                    decoration: BoxDecoration(
                      gradient: RadialGradient(
                        center: Alignment.center,
                        radius: 1.3,
                        colors: [
                          const Color(0xFF0D0B1E).withValues(alpha: dim * 0.72),
                          const Color(0xFF020109).withValues(alpha: dim * 0.97),
                        ],
                      ),
                    ),
                  ),
                ),
              // Voile de brume blanchâtre au centre (effet brouillard)
              if (dim > 0.15)
                Positioned.fill(
                  child: DecoratedBox(
                    decoration: BoxDecoration(
                      gradient: RadialGradient(
                        center: Alignment.center,
                        radius: 0.6,
                        colors: [
                          Colors.white.withValues(alpha: (dim - 0.15) * 0.06),
                          Colors.transparent,
                        ],
                      ),
                    ),
                  ),
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
