import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../generated/app_localizations.dart';
import '../services/version_check_service.dart';
import 'update_popup_celebration_view.dart';
import 'update_popup_controllers.dart';
import 'update_popup_update_view.dart';

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
  bool _isUpdating = false;
  final AudioPlayer _audioPlayer = AudioPlayer();

  @override
  void initState() {
    super.initState();
    _ctrl = UpdatePopupControllers.create(this);
    _ctrl.ambient.repeat();
    _ctrl.shimmer.repeat();

    if (widget.mode == UpdatePopupMode.celebration) {
      _ctrl.entry.forward(); // ampoule visible immédiatement en mode celebration
      _isUpdating = true;
      _runCelebration();
    } else {
      _startFlicker(); // entry.forward() appelé en fin de séquence, après le brouillard
    }
  }

  // ── Mode update ──────────────────────────────────────────────────────────────

  void _startFlicker() async {
    // Ampoule visible sur fond transparent — petite pause avant de grésiller
    await Future.delayed(const Duration(milliseconds: 600));
    if (!mounted || _isUpdating) return;

    // Son de grésillage + 3 flashs rapides (80 ms aller + 80 ms retour)
    await _audioPlayer.play(AssetSource('sounds/ampoule-qui-eclate.ogg'));
    for (int i = 0; i < 3; i++) {
      await _ctrl.flicker.forward();
      await _ctrl.flicker.reverse();
      if (!mounted) return;
      if (i < 2) await Future.delayed(const Duration(milliseconds: 110));
    }

    // Burst : ampoule au maximum, puis brouillard s'installe
    await _ctrl.flicker.forward();
    await Future.delayed(const Duration(milliseconds: 80));
    if (!mounted) return;
    _ctrl.fogIn.forward();

    // Titre + boutons émergent du brouillard
    await Future.delayed(const Duration(milliseconds: 380));
    if (!mounted) return;
    _ctrl.entry.forward();
  }

  Future<void> _onUpdate() async {
    if (_isUpdating) return;
    setState(() => _isUpdating = true);
    _ctrl.flicker.stop();
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
    // Ampoule grisée visible — le brouillard s'installe (500 ms via barrierColor)
    await Future.delayed(const Duration(milliseconds: 500));
    if (!mounted) return;

    // Unique scintillement silencieux (tentative d'allumage)
    await _ctrl.flicker.forward();
    await _ctrl.flicker.reverse();
    if (!mounted) return;
    await Future.delayed(const Duration(milliseconds: 120));
    if (!mounted) return;

    // Allumage + dégagement du brouillard + halos solaires (simultanés)
    _ctrl.light.forward();
    await Future.delayed(const Duration(milliseconds: 180));
    if (!mounted) return;
    _ctrl.clear.forward(); // repousse les volutes au moment du burst
    await _ctrl.halo.forward();

    await Future.delayed(const Duration(milliseconds: 400));
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
    if (widget.mode == UpdatePopupMode.celebration) {
      return CelebrationModeView(ctrl: _ctrl);
    }
    return UpdateModeView(
      ctrl: _ctrl,
      loc: AppLocalizations.of(context)!,
      isUpdating: _isUpdating,
      onUpdate: _onUpdate,
      onLater: widget.onLater != null ? _onLater : null,
    );
  }
}
