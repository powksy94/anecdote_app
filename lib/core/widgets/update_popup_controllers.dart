import 'package:flutter/material.dart';

/// Contient et initialise tous les AnimationControllers + animations dérivées
/// du popup de mise à jour.
class UpdatePopupControllers {
  // Entrée
  final AnimationController entry;
  final Animation<double> entryScale;
  final Animation<double> entryOpacity;

  // Flicker (mode update — idle)
  final AnimationController flicker;
  final Animation<double> flickerAnim;

  // Allumage ampoule (mode celebration)
  final AnimationController light;
  final Animation<double> scaleAnim;
  final Animation<double> glowAnim;
  final Animation<Color?> colorAnim;

  // Ambiant (étoiles + blobs + rayons)
  final AnimationController ambient;

  // Shimmer bouton
  final AnimationController shimmer;

  // Phase halos (mode celebration — 3 pulses staggerées)
  final AnimationController halo;
  final Animation<double> haloAnim1;
  final Animation<double> haloAnim2;
  final Animation<double> haloAnim3;

  UpdatePopupControllers._({
    required this.entry,      required this.entryScale,  required this.entryOpacity,
    required this.flicker,    required this.flickerAnim,
    required this.light,      required this.scaleAnim,   required this.glowAnim,
    required this.colorAnim,
    required this.ambient,    required this.shimmer,
    required this.halo,
    required this.haloAnim1,  required this.haloAnim2,   required this.haloAnim3,
  });

  factory UpdatePopupControllers.create(TickerProvider vsync) {
    // — Entrée —
    final entry = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 400));
    final entryScale = Tween<double>(begin: 0.80, end: 1.0)
        .animate(CurvedAnimation(parent: entry, curve: Curves.easeOutBack));
    final entryOpacity = Tween<double>(begin: 0.0, end: 1.0)
        .animate(CurvedAnimation(parent: entry, curve: Curves.easeOut));

    // — Flicker —
    final flicker = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 120));
    final flickerAnim = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 0.35, end: 0.65), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 0.65, end: 0.20), weight: 2),
      TweenSequenceItem(tween: Tween(begin: 0.20, end: 0.45), weight: 1),
    ]).animate(flicker);

    // — Allumage —
    final light = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 700));
    final scaleAnim = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.35), weight: 1),
      TweenSequenceItem(tween: Tween(begin: 1.35, end: 1.0), weight: 1),
    ]).animate(CurvedAnimation(parent: light, curve: Curves.easeInOut));
    final glowAnim = Tween<double>(begin: 0, end: 32)
        .animate(CurvedAnimation(parent: light, curve: Curves.easeOut));
    final colorAnim = ColorTween(begin: Colors.grey.shade400, end: Colors.amber)
        .animate(CurvedAnimation(parent: light, curve: Curves.easeIn));

    // — Ambiant / shimmer —
    final ambient = AnimationController(vsync: vsync, duration: const Duration(seconds: 6));
    final shimmer = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 2000));

    // — Halos (3 pulses staggerées sur 2.4 s) —
    final halo = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 2400));
    final haloAnim1 = CurvedAnimation(
        parent: halo, curve: const Interval(0.00, 0.35, curve: Curves.easeOut));
    final haloAnim2 = CurvedAnimation(
        parent: halo, curve: const Interval(0.22, 0.57, curve: Curves.easeOut));
    final haloAnim3 = CurvedAnimation(
        parent: halo, curve: const Interval(0.44, 0.79, curve: Curves.easeOut));

    return UpdatePopupControllers._(
      entry: entry,           entryScale: entryScale,     entryOpacity: entryOpacity,
      flicker: flicker,       flickerAnim: flickerAnim,
      light: light,           scaleAnim: scaleAnim,       glowAnim: glowAnim,
      colorAnim: colorAnim,
      ambient: ambient,       shimmer: shimmer,
      halo: halo,
      haloAnim1: haloAnim1,   haloAnim2: haloAnim2,       haloAnim3: haloAnim3,
    );
  }

  void dispose() {
    entry.dispose();
    flicker.dispose();
    light.dispose();
    ambient.dispose();
    shimmer.dispose();
    halo.dispose();
  }

}
