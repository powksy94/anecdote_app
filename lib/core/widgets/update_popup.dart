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

    // Scintillement 1
    await _audioPlayer.play(AssetSource('sounds/ampoule-qui-eclate.ogg'));
    await _ctrl.flicker.forward();
    await _ctrl.flicker.reverse();
    if (!mounted) return;
    await Future.delayed(const Duration(milliseconds: 80));
    if (!mounted) return;

    // Scintillement 2
    await _ctrl.flicker.forward();
    await _ctrl.flicker.reverse();
    if (!mounted) return;
    await Future.delayed(const Duration(milliseconds: 120));
    if (!mounted) return;

    // Allumage complet + halos solaires plein-écran
    _ctrl.light.forward();
    await Future.delayed(const Duration(milliseconds: 180));
    if (!mounted) return;
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
