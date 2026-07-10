import 'package:flutter/material.dart';

/// Contient et initialise tous les AnimationControllers + animations dérivées
/// du popup de mise à jour.
class UpdatePopupControllers {
  // Entrée
  final AnimationController entry;
  final Animation<double> entryScale;
  final Animation<double> entryOpacity;

  // Flicker (mode update — grésillements de démarrage)
  final AnimationController flicker;
  final Animation<double> flickerAnim;

  // Brouillard update (apparaît après le burst, piloté séparément)
  final AnimationController fogIn;
  final Animation<double> fogInAnim;

  // Allumage ampoule (mode celebration)
  final AnimationController light;
  final Animation<double> scaleAnim;
  final Animation<double> glowAnim;
  final Animation<Color?> colorAnim;

  // Ambiant (volutes + particules + rayons)
  final AnimationController ambient;

  // Shimmer bouton
  final AnimationController shimmer;

  // Dégagement du brouillard (mode celebration — au burst)
  final AnimationController clear;
  final Animation<double> clearAnim;

  // Halos solaires (mode celebration — 3 pulses staggerées)
  final AnimationController halo;
  final Animation<double> haloAnim1;
  final Animation<double> haloAnim2;
  final Animation<double> haloAnim3;

  UpdatePopupControllers._({
    required this.entry,      required this.entryScale,  required this.entryOpacity,
    required this.flicker,    required this.flickerAnim,
    required this.fogIn,      required this.fogInAnim,
    required this.light,      required this.scaleAnim,   required this.glowAnim,
    required this.colorAnim,
    required this.ambient,    required this.shimmer,
    required this.clear,      required this.clearAnim,
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

    // — Flicker : simple aller-retour dim→bright, 80 ms par flash —
    final flicker = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 80));
    final flickerAnim = Tween<double>(begin: 0.15, end: 0.90)
        .animate(CurvedAnimation(parent: flicker, curve: Curves.easeInOut));

    // — Blackout update : noirceur quasi-instantanée (200 ms, easeOut = rapide au début) —
    final fogIn = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 200));
    final fogInAnim = CurvedAnimation(parent: fogIn, curve: Curves.easeOut);

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

    // — Dégagement brouillard (700 ms, easeOut) —
    final clear = AnimationController(vsync: vsync, duration: const Duration(milliseconds: 700));
    final clearAnim = CurvedAnimation(parent: clear, curve: Curves.easeOut);

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
      fogIn: fogIn,           fogInAnim: fogInAnim,
      light: light,           scaleAnim: scaleAnim,       glowAnim: glowAnim,
      colorAnim: colorAnim,
      ambient: ambient,       shimmer: shimmer,
      clear: clear,           clearAnim: clearAnim,
      halo: halo,
      haloAnim1: haloAnim1,   haloAnim2: haloAnim2,       haloAnim3: haloAnim3,
    );
  }

  void dispose() {
    entry.dispose();
    flicker.dispose();
    fogIn.dispose();
    light.dispose();
    ambient.dispose();
    shimmer.dispose();
    clear.dispose();
    halo.dispose();
  }
}
