import 'dart:math' as math;
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../generated/app_localizations.dart';
import '../services/version_check_service.dart';

enum UpdatePopupMode { update, celebration }

class UpdatePopup extends StatefulWidget {
  final UpdatePopupMode mode;

  const UpdatePopup({super.key, this.mode = UpdatePopupMode.update});

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
    // Un seul flicker puis stop
    await Future.delayed(Duration(milliseconds: 800 + rng.nextInt(1200)));
    if (!mounted || _isUpdating) return;
    await _audioPlayer.play(AssetSource('ampoule-qui-eclate.ogg'));
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

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      title: Text(loc.updateTitle, textAlign: TextAlign.center),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          AnimatedBuilder(
            animation: Listenable.merge([_flickerAnim, _lightCtrl]),
            builder: (context, _) {
              final lit = _lightCtrl.value > 0;
              final opacity = lit ? 1.0 : _flickerAnim.value;
              final color = lit
                  ? (_colorAnim.value ?? Colors.amber)
                  : Colors.grey.shade400;
              final scale = lit ? _scaleAnim.value : 1.0;
              final glow = lit ? _glowAnim.value : 0.0;

              return Transform.scale(
                scale: scale,
                child: Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    boxShadow: glow > 0
                        ? [
                            BoxShadow(
                              color: Colors.amber.withValues(alpha: 0.5),
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
                      size: 64,
                      color: color,
                    ),
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 16),
          Text(
            isCelebration ? '' : loc.updateMessage,
            textAlign: TextAlign.center,
          ),
        ],
      ),
      actionsAlignment: MainAxisAlignment.center,
      actions: isCelebration
          ? []
          : [
              ElevatedButton.icon(
                onPressed: _isUpdating ? null : _onUpdate,
                icon: const Icon(Icons.download_rounded),
                label: Text(loc.updateButton),
                style: ElevatedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ],
    );
  }
}
