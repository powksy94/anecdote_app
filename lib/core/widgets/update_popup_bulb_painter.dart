import 'package:flutter/material.dart';
import 'update_popup_bulb_base.dart';
import 'update_popup_bulb_broken.dart';
import 'update_popup_bulb_globe.dart';
import 'update_popup_bulb_shards.dart';

/// Orchestre le rendu complet de l'ampoule selon sa phase :
///   - [burst] < 0.12 : ampoule entière (globe + filament + culot)
///   - [burst] ≥ 0.12 : ampoule grillée (culot + bord dentelé + fils cassés)
///   - [burst] > 0    : éclats de verre en vol parabolique
class BulbPainter extends CustomPainter {
  final double flicker;  // 0→1 luminosité sizzle (flickerAnim.value)
  final double light;    // 0→1 allumage celebration (lightCtrl.value)
  final double breathe;  // 0→1 cycle ambiant
  final double burst;    // 0→1 progression explosion

  const BulbPainter({
    required this.flicker,
    required this.light,
    required this.breathe,
    required this.burst,
  });

  static const double _gr = 33.0; // rayon du globe

  Offset _gc(Size size) => Offset(size.width / 2, size.height / 2 - 27);

  @override
  void paint(Canvas canvas, Size size) {
    final gc = _gc(size);

    if (burst < 0.12) {
      // Ampoule entière : culot + col + globe + filament + reflets
      drawBulbBase(canvas, gc, _gr);
      drawBulbNeck(canvas, gc, _gr);
      drawBulbGlobe(canvas, gc, _gr,
        flicker: flicker, light: light, breathe: breathe);
      drawBulbFilament(canvas, gc,
        broken: false, flicker: flicker, light: light);
      drawBulbGlobeOverlay(canvas, gc, _gr);
    } else {
      // Ampoule grillée : culot + col + bord dentelé + fils cassés
      drawBrokenBulb(canvas, gc, _gr);
    }

    if (burst > 0.005) {
      drawBulbShards(canvas, gc, burst);
    }
  }

  @override
  bool shouldRepaint(BulbPainter old) =>
      old.flicker != flicker ||
      old.light   != light   ||
      old.breathe != breathe ||
      old.burst   != burst;
}
