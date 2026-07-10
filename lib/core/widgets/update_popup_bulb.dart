import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'update_popup_painters.dart';

class UpdatePopupBulb extends StatelessWidget {
  final Animation<double> flickerAnim;
  final AnimationController lightCtrl;
  final Animation<double> scaleAnim;
  final Animation<double> glowAnim;
  final Animation<Color?> colorAnim;
  final AnimationController ambientCtrl;

  /// Tap sur l'ampoule — déclenche la mise à jour (mode update uniquement).
  final VoidCallback? onTap;

  const UpdatePopupBulb({
    super.key,
    required this.flickerAnim,
    required this.lightCtrl,
    required this.scaleAnim,
    required this.glowAnim,
    required this.colorAnim,
    required this.ambientCtrl,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedBuilder(
        animation: Listenable.merge([flickerAnim, lightCtrl, ambientCtrl]),
        builder: (context, _) {
          final lit = lightCtrl.value > 0;
          final opacity = (lit ? 1.0 : flickerAnim.value).clamp(0.0, 1.0);
          final bulbColor = lit ? (colorAnim.value ?? Colors.amber) : Colors.grey.shade300;
          final scale = lit ? scaleAnim.value : 1.0;
          final glow = lit ? glowAnim.value : 0.0;
          final rayRotation = ambientCtrl.value * 2 * math.pi;

          // Rayons plus visibles quand allumé, subtils mais présents à l'idle
          final raysAlpha = lit ? 0.80 : (flickerAnim.value * 0.55).clamp(0.18, 0.55);

          // Halo violet ambiant qui respire — s'intensifie lors des grésillements
          final ambientGlow = lit
              ? 0.0
              : (math.sin(ambientCtrl.value * 2 * math.pi) + 1) / 2 * 8
                + (flickerAnim.value - 0.15) * 6; // boost pendant les flashs

          return SizedBox(
            width: 150,
            height: 150,
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Rayons rotatifs
                Transform.rotate(
                  angle: rayRotation,
                  child: CustomPaint(
                    painter: RaysPainter(
                      color: Colors.amber.withValues(alpha: raysAlpha),
                    ),
                    child: const SizedBox(width: 150, height: 150),
                  ),
                ),

                // Halo violet ambiant (respire + boost flicker)
                if (ambientGlow > 0)
                  Container(
                    width: 110,
                    height: 110,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF6D28D9).withValues(alpha: 0.45),
                          blurRadius: ambientGlow * 3,
                          spreadRadius: ambientGlow * 0.6,
                        ),
                      ],
                    ),
                  ),

                // Halo amber (allumage celebration)
                if (glow > 0)
                  Container(
                    width: 110,
                    height: 110,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.amber.withValues(alpha: 0.55),
                          blurRadius: glow * 1.8,
                          spreadRadius: glow * 0.4,
                        ),
                      ],
                    ),
                  ),

                // Globe en verre
                Transform.scale(
                  scale: scale,
                  child: Container(
                    width: 86,
                    height: 86,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      // Gradient radial décalé → effet globe de verre
                      gradient: RadialGradient(
                        center: const Alignment(-0.3, -0.4),
                        radius: 1.0,
                        colors: [
                          Colors.white.withValues(alpha: lit ? 0.20 : 0.12),
                          Colors.white.withValues(alpha: 0.02),
                        ],
                      ),
                      border: Border.all(
                        color: Colors.white.withValues(alpha: 0.24),
                        width: 1.5,
                      ),
                      boxShadow: glow > 0
                          ? [
                              BoxShadow(
                                color: Colors.amber.withValues(alpha: 0.65),
                                blurRadius: glow,
                                spreadRadius: glow / 6,
                              ),
                            ]
                          : [],
                    ),
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        // Reflet du verre (highlight spot, coin supérieur gauche)
                        Positioned(
                          left: 17,
                          top: 11,
                          child: Container(
                            width: 20,
                            height: 13,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(8),
                              color: Colors.white.withValues(alpha: 0.28),
                            ),
                          ),
                        ),
                        // Icône ampoule
                        Opacity(
                          opacity: opacity,
                          child: Icon(
                            lit ? Icons.lightbulb : Icons.lightbulb_outline,
                            size: 52,
                            color: bulbColor,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
