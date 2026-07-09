import 'dart:math' as math;
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../generated/app_localizations.dart';
import '../services/version_check_service.dart';

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
  late final AnimationController _flickerCtrl;
  late final Animation<double> _flickerAnim;

  late final AnimationController _lightCtrl;
  late final Animation<double> _scaleAnim;
  late final Animation<double> _glowAnim;
  late final Animation<Color?> _colorAnim;

  bool _isUpdating = false;
  final AudioPlayer _audioPlayer = AudioPlayer();

  @override
  void initState() {
    super.initState();

    _flickerCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 120),
    );
    _flickerAnim = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 0.35, end: 0.65), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 0.65, end: 0.20), weight: 2),
      TweenSequenceItem(tween: Tween(begin: 0.20, end: 0.45), weight: 1),
    ]).animate(_flickerCtrl);

    _lightCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 700),
    );
    _scaleAnim = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.35), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 1.35, end: 1.0), weight: 1),
    ]).animate(CurvedAnimation(parent: _lightCtrl, curve: Curves.easeInOut));
    _glowAnim = Tween<double>(begin: 0, end: 32)
        .animate(CurvedAnimation(parent: _lightCtrl, curve: Curves.easeOut));
    _colorAnim = ColorTween(begin: Colors.grey.shade400, end: Colors.amber)
        .animate(CurvedAnimation(parent: _lightCtrl, curve: Curves.easeIn));

    if (widget.mode == UpdatePopupMode.celebration) {
      _isUpdating = true;
      Future.microtask(() async {
        await _lightCtrl.forward();
        await Future.delayed(const Duration(milliseconds: 300));
        if (mounted) Navigator.pop(context);
      });
    } else {
      _startFlicker();
    }
  }

  void _startFlicker() async {
    final rng = math.Random();
    await Future.delayed(Duration(milliseconds: 800 + rng.nextInt(1200)));
    if (!mounted || _isUpdating) return;
    await _audioPlayer.play(AssetSource('sounds/ampoule-qui-eclate.ogg'));
    await _flickerCtrl.forward();
    await _flickerCtrl.reverse();
  }

  Future<void> _onUpdate() async {
    setState(() => _isUpdating = true);
    _flickerCtrl.stop();
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

  @override
  void dispose() {
    _flickerCtrl.dispose();
    _lightCtrl.dispose();
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final isCelebration = widget.mode == UpdatePopupMode.celebration;

    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.symmetric(horizontal: 32, vertical: 24),
      child: Container(
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF3730A3), Color(0xFF6D28D9)],
          ),
          borderRadius: BorderRadius.circular(24),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF3730A3).withValues(alpha: 0.5),
              blurRadius: 40,
              spreadRadius: 4,
              offset: const Offset(0, 12),
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(28, 36, 28, 28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildBulb(),
              const SizedBox(height: 24),
              if (!isCelebration) ...[
                Text(
                  loc.updateTitle,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    height: 1.3,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  loc.updateMessage,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.white.withValues(alpha: 0.8),
                    fontSize: 14,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 28),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _isUpdating ? null : _onUpdate,
                    icon: const Icon(Icons.download_rounded),
                    label: Text(loc.updateButton),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.amber.shade600,
                      foregroundColor: Colors.black87,
                      disabledBackgroundColor: Colors.amber.shade200,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(14),
                      ),
                      textStyle: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
                if (widget.onLater != null) ...[
                  const SizedBox(height: 10),
                  TextButton(
                    onPressed: _isUpdating ? null : _onLater,
                    child: Text(
                      loc.updateLaterButton,
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.6),
                        fontSize: 14,
                      ),
                    ),
                  ),
                ],
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildBulb() {
    return AnimatedBuilder(
      animation: Listenable.merge([_flickerAnim, _lightCtrl]),
      builder: (context, _) {
        final lit = _lightCtrl.value > 0;
        final opacity = lit ? 1.0 : _flickerAnim.value;
        final color = lit
            ? (_colorAnim.value ?? Colors.amber)
            : Colors.grey.shade300;
        final scale = lit ? _scaleAnim.value : 1.0;
        final glow = lit ? _glowAnim.value : 0.0;

        return Transform.scale(
          scale: scale,
          child: Container(
            width: 88,
            height: 88,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: Colors.white.withValues(alpha: 0.12),
              boxShadow: glow > 0
                  ? [
                      BoxShadow(
                        color: Colors.amber.withValues(alpha: 0.6),
                        blurRadius: glow,
                        spreadRadius: glow / 4,
                      ),
                    ]
                  : [],
            ),
            child: Opacity(
              opacity: opacity,
              child: Icon(
                lit ? Icons.lightbulb : Icons.lightbulb_outline,
                size: 52,
                color: color,
              ),
            ),
          ),
        );
      },
    );
  }
}
