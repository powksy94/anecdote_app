import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'update_popup.dart';

/// Affiche le popup de mise à jour.
/// Le brouillard est géré par UpdateFog à l'intérieur du widget,
/// déclenché après le grésillage de l'ampoule.
Future<T?> showUpdateFogDialog<T>(
  BuildContext context, {
  VoidCallback? onLater,
}) {
  return showGeneralDialog<T>(
    context: context,
    barrierDismissible: false,
    barrierColor: Colors.transparent,
    transitionDuration: Duration.zero,
    // Material fix : sans ce wrapper les Text héritent d'un style sans contexte
    // (TextStyle avec soulignement jaune — comportement Flutter par défaut hors Material).
    pageBuilder: (ctx, _, __) => Material(
      color: Colors.transparent,
      child: UpdatePopup(mode: UpdatePopupMode.update, onLater: onLater),
    ),
  );
}

/// Affiche la célébration post-mise-à-jour.
Future<T?> showCelebrationDialog<T>(BuildContext context) {
  return showGeneralDialog<T>(
    context: context,
    barrierDismissible: false,
    barrierColor: Colors.transparent,
    transitionDuration: Duration.zero,
    pageBuilder: (ctx, _, __) => const Material(
      color: Colors.transparent,
      child: UpdatePopup(mode: UpdatePopupMode.celebration),
    ),
  );
}

/// Fond sombre + volutes animées pour le mode update.
/// Opacité pilotée par [fogInAnim] (0→1 après le burst de l'ampoule).
class UpdateFog extends StatelessWidget {
  final Animation<double> fogInAnim;
  final AnimationController ambientCtrl;

  const UpdateFog({
    super.key,
    required this.fogInAnim,
    required this.ambientCtrl,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: Listenable.merge([fogInAnim, ambientCtrl]),
      builder: (_, __) => CustomPaint(
        painter: _FogPainter(fogInAnim.value, ambientCtrl.value),
        child: const SizedBox.expand(),
      ),
    );
  }
}

/// Peint un fond sombre et 5 volutes de brume en orbite elliptique.
class _FogPainter extends CustomPainter {
  final double fogOpacity; // 0 → 1 piloté par fogIn
  final double fog;        // cycle continu 0 → 1 pour les orbites

  const _FogPainter(this.fogOpacity, this.fog);

  @override
  void paint(Canvas canvas, Size size) {
    if (fogOpacity <= 0) return;

    final w = size.width;
    final h = size.height;

    final basePaint = Paint()
      ..shader = RadialGradient(
        center: Alignment.center,
        radius: 1.6,
        colors: [
          const Color(0xFF0D0B1E).withValues(alpha: fogOpacity * 0.83),
          const Color(0xFF020109).withValues(alpha: fogOpacity * 0.97),
        ],
      ).createShader(Rect.fromLTWH(0, 0, w, h));
    canvas.drawRect(Rect.fromLTWH(0, 0, w, h), basePaint);

    if (fogOpacity < 0.25) return;
    final fa = ((fogOpacity - 0.25) / 0.75).clamp(0.0, 1.0);

    final a = fog * math.pi * 2;

    _drawWisp(canvas, size,
      cx: w * 0.22 + math.sin(a) * w * 0.12,
      cy: h * 0.28 + math.cos(a) * h * 0.07,
      rx: w * 0.48, ry: h * 0.20,
      color: const Color(0xFFB8A0FF), alpha: fa * 0.13,
    );

    final a2 = a + 2.094;
    _drawWisp(canvas, size,
      cx: w * 0.72 + math.sin(a2) * w * 0.10,
      cy: h * 0.50 - math.cos(a2) * h * 0.09,
      rx: w * 0.44, ry: h * 0.18,
      color: const Color(0xFF8060CC), alpha: fa * 0.15,
    );

    final a3 = a + 4.189;
    _drawWisp(canvas, size,
      cx: w * 0.45 + math.sin(a3) * w * 0.09,
      cy: h * 0.72 + math.cos(a3) * h * 0.06,
      rx: w * 0.58, ry: h * 0.24,
      color: const Color(0xFF7040B8), alpha: fa * 0.12,
    );

    final a4 = a + 1.047;
    _drawWisp(canvas, size,
      cx: w * 0.50 + math.sin(a4) * w * 0.05,
      cy: h * 0.44 - math.cos(a4) * h * 0.04,
      rx: w * 0.40, ry: h * 0.30,
      color: Colors.white, alpha: fa * 0.07,
    );

    final a5 = fog * math.pi * 4 + math.pi;
    _drawWisp(canvas, size,
      cx: w * 0.80 + math.sin(a5) * w * 0.08,
      cy: h * 0.18 - math.cos(a5) * h * 0.07,
      rx: w * 0.30, ry: h * 0.14,
      color: const Color(0xFFD0B8FF), alpha: fa * 0.10,
    );
  }

  void _drawWisp(
    Canvas canvas, Size size, {
    required double cx, required double cy,
    required double rx, required double ry,
    required Color color, required double alpha,
  }) {
    final rect = Rect.fromCenter(center: Offset(cx, cy), width: rx * 2, height: ry * 2);
    canvas.drawOval(
      rect,
      Paint()
        ..shader = RadialGradient(
          colors: [
            color.withValues(alpha: alpha),
            color.withValues(alpha: alpha * 0.45),
            Colors.transparent,
          ],
          stops: const [0.0, 0.5, 1.0],
        ).createShader(rect),
    );
  }

  @override
  bool shouldRepaint(_FogPainter old) =>
      old.fogOpacity != fogOpacity || old.fog != fog;
}
