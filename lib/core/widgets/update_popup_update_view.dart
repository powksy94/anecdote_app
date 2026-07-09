import 'package:flutter/material.dart';
import '../../generated/app_localizations.dart';
import 'update_popup_bulb.dart';
import 'update_popup_content.dart';
import 'update_popup_controllers.dart';

/// Vue plein-écran pour le mode update : ampoule + texte + boutons
/// flottant sur le brouillard géré par showUpdateFogDialog.
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
    return ListenableBuilder(
      listenable: ctrl.entry,
      builder: (context, child) => Opacity(
        opacity: ctrl.entryOpacity.value,
        child: Transform.scale(scale: ctrl.entryScale.value, child: child),
      ),
      child: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: [
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
                UpdatePopupContent(
                  loc: loc,
                  shimmerCtrl: ctrl.shimmer,
                  isUpdating: isUpdating,
                  onUpdate: onUpdate,
                  onLater: onLater,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
