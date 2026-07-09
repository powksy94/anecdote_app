import 'dart:math' as math;
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../generated/app_localizations.dart';
import '../services/version_check_service.dart';
import 'update_popup_background.dart';
import 'update_popup_bulb.dart';
import 'update_popup_content.dart';
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
  late final AnimationController _entryCtrl;
  late final Animation<double> _entryScale;
  late final Animation<double> _entryOpacity;

  late final AnimationController _flickerCtrl;
  late final Animation<double> _flickerAnim;

  late final AnimationController _lightCtrl;
  late final Animation<double> _scaleAnim;
  late final Animation<double> _glowAnim;
  late final Animation<Color?> _colorAnim;

  late final AnimationController _ambientCtrl;
  late final AnimationController _shimmerCtrl;

  bool _isUpdating = false;
  final AudioPlayer _audioPlayer = AudioPlayer();
  late final List<StarData> _stars;

  @override
  void initState() {
    super.initState();

    _stars = _buildStars();

    _entryCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 400));
    _entryScale = Tween<double>(begin: 0.80, end: 1.0)
        .animate(CurvedAnimation(parent: _entryCtrl, curve: Curves.easeOutBack));
    _entryOpacity = Tween<double>(begin: 0.0, end: 1.0)
        .animate(CurvedAnimation(parent: _entryCtrl, curve: Curves.easeOut));
    _entryCtrl.forward();

    _flickerCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 120));
    _flickerAnim = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 0.35, end: 0.65), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 0.65, end: 0.20), weight: 2),
      TweenSequenceItem(tween: Tween(begin: 0.20, end: 0.45), weight: 1),
    ]).animate(_flickerCtrl);

    _lightCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 700));
    _scaleAnim = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.35), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 1.35, end: 1.0), weight: 1),
    ]).animate(CurvedAnimation(parent: _lightCtrl, curve: Curves.easeInOut));
    _glowAnim = Tween<double>(begin: 0, end: 32)
        .animate(CurvedAnimation(parent: _lightCtrl, curve: Curves.easeOut));
    _colorAnim = ColorTween(begin: Colors.grey.shade400, end: Colors.amber)
        .animate(CurvedAnimation(parent: _lightCtrl, curve: Curves.easeIn));

    _ambientCtrl = AnimationController(vsync: this, duration: const Duration(seconds: 6))
      ..repeat();
    _shimmerCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 2000))
      ..repeat();

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

  static List<StarData> _buildStars() {
    final rng = math.Random(42);
    return List.generate(16, (i) => StarData(
      x: rng.nextDouble(),
      y: rng.nextDouble(),
      size: 1.0 + rng.nextDouble() * 2.2,
      opacity: 0.2 + rng.nextDouble() * 0.55,
      phase: rng.nextDouble(),
    ));
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
    _entryCtrl.dispose();
    _flickerCtrl.dispose();
    _lightCtrl.dispose();
    _ambientCtrl.dispose();
    _shimmerCtrl.dispose();
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final isCelebration = widget.mode == UpdatePopupMode.celebration;

    return ListenableBuilder(
      listenable: _entryCtrl,
      builder: (context, child) => Opacity(
        opacity: _entryOpacity.value,
        child: Transform.scale(scale: _entryScale.value, child: child),
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
                UpdatePopupBackground(ambientCtrl: _ambientCtrl, stars: _stars),
                Padding(
                  padding: const EdgeInsets.fromLTRB(28, 44, 28, 32),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      UpdatePopupBulb(
                        flickerAnim: _flickerAnim,
                        lightCtrl: _lightCtrl,
                        scaleAnim: _scaleAnim,
                        glowAnim: _glowAnim,
                        colorAnim: _colorAnim,
                        ambientCtrl: _ambientCtrl,
                      ),
                      if (!isCelebration) ...[
                        const SizedBox(height: 30),
                        UpdatePopupContent(
                          loc: loc,
                          shimmerCtrl: _shimmerCtrl,
                          isUpdating: _isUpdating,
                          onUpdate: _onUpdate,
                          onLater: widget.onLater != null ? _onLater : null,
                        ),
                      ],
                    ],
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
