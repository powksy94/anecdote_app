import 'package:flutter/material.dart';
import 'update_popup_bulb.dart';
import 'update_popup_controllers.dart';
import 'update_popup_halo.dart';

/// Vue plein-écran pour le mode celebration : ampoule grisée au centre
/// du brouillard, puis allumage et halos solaires rayonnants.
class CelebrationModeView extends StatelessWidget {
  final UpdatePopupControllers ctrl;

  const CelebrationModeView({super.key, required this.ctrl});

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: ctrl.entry,
      builder: (context, child) => Opacity(
        opacity: ctrl.entryOpacity.value,
        child: child,
      ),
      child: SafeArea(
        child: Stack(
          fit: StackFit.expand,
          children: [
            // Ampoule centrée (grisée au départ, s'allume via ctrl.light)
            Center(
              child: UpdatePopupBulb(
                flickerAnim: ctrl.flickerAnim,
                lightCtrl: ctrl.light,
                scaleAnim: ctrl.scaleAnim,
                glowAnim: ctrl.glowAnim,
                colorAnim: ctrl.colorAnim,
                ambientCtrl: ctrl.ambient,
              ),
            ),
            // Halos solaires plein-écran (ring + 12 rayons triangulaires)
            Positioned.fill(
              child: UpdatePopupHalo(
                pulses: [ctrl.haloAnim1, ctrl.haloAnim2, ctrl.haloAnim3],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
