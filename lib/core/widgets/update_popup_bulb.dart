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
          final raysAlpha = lit ? 0.75 : 0.20;
          final ambientGlow = lit
              ? 0.0
              : (math.sin(ambientCtrl.value * 2 * math.pi) + 1) / 2 * 6;

          return SizedBox(
            width: 130,
            height: 130,
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
                    child: const SizedBox(width: 130, height: 130),
                  ),
                ),
                // Halo violet ambiant (respire doucement à l'idle)
                if (ambientGlow > 0)
                  Container(
                    width: 90,
                    height: 90,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF6D28D9).withValues(alpha: 0.4),
                          blurRadius: ambientGlow * 3,
                          spreadRadius: ambientGlow * 0.5,
                        ),
                      ],
                    ),
                  ),
                // Halo amber (allumage)
                if (glow > 0)
                  Container(
                    width: 90,
                    height: 90,
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
                // Ampoule
                Transform.scale(
                  scale: scale,
                  child: Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: Colors.white.withValues(alpha: 0.07),
                      border: Border.all(
                        color: Colors.white.withValues(alpha: 0.14),
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
                    child: Opacity(
                      opacity: opacity,
                      child: Icon(
                        lit ? Icons.lightbulb : Icons.lightbulb_outline,
                        size: 44,
                        color: bulbColor,
                      ),
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
