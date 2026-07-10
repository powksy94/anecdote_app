import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'update_popup_bulb_painter.dart';
import 'update_popup_painters.dart';

class UpdatePopupBulb extends StatelessWidget {
  final Animation<double> flickerAnim;
  final AnimationController lightCtrl;
  final Animation<double> scaleAnim;
  final Animation<double> glowAnim;
  final Animation<Color?> colorAnim;
  final AnimationController ambientCtrl;
  final AnimationController burstCtrl;

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
    required this.burstCtrl,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedBuilder(
        animation: Listenable.merge([flickerAnim, lightCtrl, ambientCtrl, burstCtrl]),
        builder: (context, _) {
          final lit    = lightCtrl.value > 0;
          final burst  = burstCtrl.value;
          final glow   = lit ? glowAnim.value : 0.0;
          final rayRotation = ambientCtrl.value * 2 * math.pi;

          // Rayons : visibles avant l'explosion seulement
          final raysAlpha = burst > 0.05
              ? 0.0
              : lit
                  ? 0.80
                  : (flickerAnim.value * 0.55).clamp(0.18, 0.55);

          // Halo violet ambiant qui respire — s'intensifie lors des grésillements
          final ambientGlow = (lit || burst > 0.05)
              ? 0.0
              : (math.sin(ambientCtrl.value * 2 * math.pi) + 1) / 2 * 8
                + (flickerAnim.value - 0.15) * 6;

          return SizedBox(
            width: 150,
            height: 200,
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Rayons rotatifs (disparaissent au burst)
                if (raysAlpha > 0)
                  Transform.rotate(
                    angle: rayRotation,
                    // Pivot = centre du globe dans le SizedBox 150×200 :
                    // y_globe = 100 − 27 = 73 → alignment.y = (73−100)/100 = −0.27
                    alignment: const Alignment(0, -0.27),
                    child: CustomPaint(
                      painter: RaysPainter(
                        color: Colors.amber.withValues(alpha: raysAlpha),
                        centerDy: -27,
                      ),
                      child: const SizedBox(width: 150, height: 200),
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

                // Ampoule 3D (BulbPainter — globe, filament, culot, éclats)
                CustomPaint(
                  painter: BulbPainter(
                    flicker: flickerAnim.value,
                    light:   lightCtrl.value,
                    breathe: ambientCtrl.value,
                    burst:   burst,
                  ),
                  child: const SizedBox(width: 150, height: 200),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
