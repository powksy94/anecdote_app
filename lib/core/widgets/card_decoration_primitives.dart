part of 'card_decorations.dart';

Widget _circle(double size, Color color) => Container(
      width: size,
      height: size,
      decoration: BoxDecoration(shape: BoxShape.circle, color: color),
    );

Widget _rect(double width, double height, Color color) => Container(
      width: width,
      height: height,
      decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(8)),
    );

Widget _icon(IconData icon, double size, double opacity) =>
    Icon(icon, size: size, color: Colors.white.withValues(alpha: opacity));
