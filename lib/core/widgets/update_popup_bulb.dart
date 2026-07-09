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

  /// Quand [dimmingAnim] progresse (0→1), l'ampoule s'éteint progressivement.
  final Animation<double>? dimmingAnim;

  /// Tap sur l'ampoule — déclenche la mise à jour (identique au bouton principal).
  final VoidCallback? onTap;

  const UpdatePopupBulb({
    super.key,
    required this.flickerAnim,
    required this.lightCtrl,
    required this.scaleAnim,
    required this.glowAnim,
    required this.colorAnim,
    required this.ambientCtrl,
    this.dimmingAnim,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final listenables = <Listenable>[flickerAnim, lightCtrl, ambientCtrl];
    if (dimmingAnim != null) listenables.add(dimmingAnim!);

    return GestureDetector(
      onTap: onTap,
      child: AnimatedBuilder(
        animation: Listenable.merge(listenables),
        builder: (context, _) {
          final lit = lightCtrl.value > 0;
          final dim = dimmingAnim?.value ?? 0.0;

          // L'ampoule s'éteint au fur et à mesure du dimming
          final rawOpacity = lit ? 1.0 : flickerAnim.value;
          final opacity = (rawOpacity * (1.0 - dim * 0.92)).clamp(0.0, 1.0);

          final bulbColor = lit ? (colorAnim.value ?? Colors.amber) : Colors.grey.shade300;
          final scale = lit ? scaleAnim.value : 1.0;
          final glow = lit ? glowAnim.value * (1.0 - dim) : 0.0;
          final rayRotation = ambientCtrl.value * 2 * math.pi;
          final raysAlpha = (lit ? 0.75 : 0.20) * (1.0 - dim);
          final ambientGlow = (lit || dim > 0.05)
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
                  child: Opacity(
                    opacity: (1.0 - dim).clamp(0.0, 1.0),
                    child: CustomPaint(
                      painter: RaysPainter(
                        color: Colors.amber.withValues(alpha: raysAlpha),
                      ),
                      child: const SizedBox(width: 130, height: 130),
                    ),
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
                      color: Colors.white.withValues(alpha: 0.07 * (1 - dim)),
                      border: Border.all(
                        color: Colors.white.withValues(alpha: 0.14 * (1 - dim)),
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
