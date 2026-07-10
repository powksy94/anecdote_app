import 'package:flutter/material.dart';
import 'update_popup_bulb.dart';
import 'update_popup_celebration_fog.dart';
import 'update_popup_controllers.dart';
import 'update_popup_halo.dart';

/// Vue plein-écran pour le mode celebration :
///   - Brouillard vivant (volutes + particules) qui couvre tout l'écran
///   - Ampoule grisée → scintillement → allumage
///   - 3 halos solaires en parallaxe qui explosent plein-écran
///   - Volutes repoussées radialement au burst (effet CoC "nuages qui s'écartent")
class CelebrationModeView extends StatelessWidget {
  final UpdatePopupControllers ctrl;

  const CelebrationModeView({super.key, required this.ctrl});

  @override
  Widget build(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        // Brouillard plein-écran (sans SafeArea — couvre status bar et nav bar)
        CelebrationFog(
          ambientCtrl: ctrl.ambient,
          clearAnim: ctrl.clearAnim,
        ),

        // Halos solaires plein-écran centrés sur le globe de l'ampoule
        Positioned.fill(
          child: Builder(
            builder: (context) {
              final p = MediaQuery.of(context).padding;
              // Globe = centre SafeArea − 27 px (offset dans BulbPainter)
              final centerDy = (p.top - p.bottom) / 2 - 27;
              return UpdatePopupHalo(
                pulses: [ctrl.haloAnim1, ctrl.haloAnim2, ctrl.haloAnim3],
                centerDy: centerDy,
              );
            },
          ),
        ),

        // Ampoule centrée avec SafeArea + fade-in via ctrl.entry
        SafeArea(
          child: Center(
            child: ListenableBuilder(
              listenable: ctrl.entry,
              builder: (_, child) =>
                  Opacity(opacity: ctrl.entryOpacity.value, child: child),
              child: UpdatePopupBulb(
                flickerAnim: ctrl.flickerAnim,
                lightCtrl: ctrl.light,
                scaleAnim: ctrl.scaleAnim,
                glowAnim: ctrl.glowAnim,
                colorAnim: ctrl.colorAnim,
                ambientCtrl: ctrl.ambient,
                burstCtrl: ctrl.burst,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
