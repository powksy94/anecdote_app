import 'package:flutter/material.dart';
import '../../generated/app_localizations.dart';
import 'update_popup_bulb.dart';
import 'update_popup_content.dart';
import 'update_popup_controllers.dart';
import 'update_popup_fog.dart';

/// Vue plein-écran pour le mode update.
/// L'ampoule est visible dès l'ouverture (sur fond transparent).
/// Après le grésillage, le brouillard entre et le contenu (titre + boutons)
/// apparaît par-dessus.
class UpdateModeView extends StatelessWidget {
  final UpdatePopupControllers ctrl;
  final AppLocalizations loc;
  final bool isUpdating;
  final VoidCallback onUpdate;
  final VoidCallback? onLater;

  const UpdateModeView({
    super.key,
    required this.ctrl,
    required this.loc,
    required this.isUpdating,
    required this.onUpdate,
    this.onLater,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        // Brouillard plein-écran — invisible au départ, s'installe après le burst
        UpdateFog(fogInAnim: ctrl.fogInAnim, ambientCtrl: ctrl.ambient),

        // Contenu centré
        SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Ampoule — visible dès l'ouverture, avant le brouillard
                  UpdatePopupBulb(
                    flickerAnim: ctrl.flickerAnim,
                    lightCtrl: ctrl.light,
                    scaleAnim: ctrl.scaleAnim,
                    glowAnim: ctrl.glowAnim,
                    colorAnim: ctrl.colorAnim,
                    ambientCtrl: ctrl.ambient,
                    onTap: onUpdate,
                  ),
                  const SizedBox(height: 30),
                  // Contenu (titre + boutons) — apparaît dans le brouillard
                  ListenableBuilder(
                    listenable: ctrl.entry,
                    builder: (_, child) => Opacity(
                      opacity: ctrl.entryOpacity.value,
                      child: child,
                    ),
                    child: UpdatePopupContent(
                      loc: loc,
                      shimmerCtrl: ctrl.shimmer,
                      isUpdating: isUpdating,
                      onUpdate: onUpdate,
                      onLater: onLater,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}
