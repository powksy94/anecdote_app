import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../generated/app_localizations.dart';
import '../services/version_check_service.dart';
import 'update_popup_background.dart';
import 'update_popup_bulb.dart';
import 'update_popup_content.dart';
import 'update_popup_controllers.dart';
import 'update_popup_halo.dart';
import 'update_popup_painters.dart';

enum UpdatePopupMode { update, celebration }

class UpdatePopup extends StatefulWidget {
  final UpdatePopupMode mode;
  final VoidCallback? onLater;

  const UpdatePopup({
    super.key,
    this.mode = UpdatePopupMode.update,
    this.onLater,
  });

  static const _storeUrl =
      'https://play.google.com/store/apps/details?id=com.uzan.dailyfacts';

  @override
  State<UpdatePopup> createState() => _UpdatePopupState();
}

class _UpdatePopupState extends State<UpdatePopup> with TickerProviderStateMixin {
  late final UpdatePopupControllers _ctrl;
  late final List<StarData> _stars;
  bool _isUpdating = false;
  final AudioPlayer _audioPlayer = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _ctrl = UpdatePopupControllers.create(this);
    _stars = UpdatePopupControllers.buildStars();

    _ctrl.entry.forward();
    _ctrl.ambient.repeat();
    _ctrl.shimmer.repeat();

    if (widget.mode == UpdatePopupMode.celebration) {
      _isUpdating = true;
      _runCelebration();
    } else {
      _startFlicker();
    }
  }

  // ── Mode update ──────────────────────────────────────────────────────────────

  void _startFlicker() async {
    await Future.delayed(Duration(milliseconds: 800 + (DateTime.now().millisecond % 1200)));
    if (!mounted || _isUpdating) return;
    await _audioPlayer.play(AssetSource('sounds/ampoule-qui-eclate.ogg'));
    await _ctrl.flicker.forward();
    await _ctrl.flicker.reverse();
  }

  Future<void> _onUpdate() async {
    if (_isUpdating) return;
    setState(() => _isUpdating = true);
    _ctrl.flicker.stop();

    // Phase 1 : brouillard sombre — l'app plonge dans le quasi-noir
    await _ctrl.dimming.forward();

    await VersionCheckService.markJustUpdated();
    final uri = Uri.parse(UpdatePopup._storeUrl);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
    if (mounted) Navigator.pop(context);
  }

  void _onLater() {
    widget.onLater?.call();
    Navigator.pop(context);
  }

  // ── Mode celebration ─────────────────────────────────────────────────────────

  Future<void> _runCelebration() async {
    _ctrl.light.forward(); // ampoule s'allume en parallèle
    await Future.delayed(const Duration(milliseconds: 150));
    await _ctrl.halo.forward(); // 3 halos rayonnants (2.4 s)
    await Future.delayed(const Duration(milliseconds: 250));
    if (mounted) Navigator.pop(context);
  }

  // ── Lifecycle ────────────────────────────────────────────────────────────────

  @override
  void dispose() {
    _ctrl.dispose();
    _audioPlayer.dispose();
    super.dispose();
  }

  // ── Build ────────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final isCelebration = widget.mode == UpdatePopupMode.celebration;

    return ListenableBuilder(
      listenable: _ctrl.entry,
      builder: (context, child) => Opacity(
        opacity: _ctrl.entryOpacity.value,
        child: Transform.scale(scale: _ctrl.entryScale.value, child: child),
      ),
      child: Dialog(
        backgroundColor: Colors.transparent,
        insetPadding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 380),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(28),
            child: Stack(
              children: [
                UpdatePopupBackground(
                  ambientCtrl: _ctrl.ambient,
                  stars: _stars,
                  dimmingAnim: isCelebration ? null : _ctrl.dimmingAnim,
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(28, 44, 28, 32),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      UpdatePopupBulb(
                        flickerAnim: _ctrl.flickerAnim,
                        lightCtrl: _ctrl.light,
                        scaleAnim: _ctrl.scaleAnim,
                        glowAnim: _ctrl.glowAnim,
                        colorAnim: _ctrl.colorAnim,
                        ambientCtrl: _ctrl.ambient,
                        dimmingAnim: isCelebration ? null : _ctrl.dimmingAnim,
                        onTap: isCelebration ? null : _onUpdate,
                      ),
                      if (!isCelebration) ...[
                        const SizedBox(height: 30),
                        UpdatePopupContent(
                          loc: loc,
                          shimmerCtrl: _ctrl.shimmer,
                          isUpdating: _isUpdating,
                          onUpdate: _onUpdate,
                          onLater: widget.onLater != null ? _onLater : null,
                        ),
                      ],
                    ],
                  ),
                ),
                if (isCelebration)
                  Positioned.fill(
                    child: UpdatePopupHalo(
                      pulses: [_ctrl.haloAnim1, _ctrl.haloAnim2, _ctrl.haloAnim3],
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
