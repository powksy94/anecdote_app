part of 'card_decorations.dart';

Widget _anecdoteDecoration() => Stack(
      children: [
        Positioned(top: -20, right: -20, child: _circle(60, Colors.white.withValues(alpha: 0.10))),
        Positioned(bottom: -30, left: -30, child: _circle(80, Colors.white.withValues(alpha: 0.08))),
        Positioned(top: 20, left: 10, child: _icon(Icons.star, 12, 0.30)),
        Positioned(bottom: 40, right: 20, child: _icon(Icons.star, 8, 0.25)),
      ],
    );

Widget _historyDecoration() => Stack(
      children: [
        Positioned(
          top: 10, right: -20,
          child: Transform.rotate(angle: 0.2, child: _rect(60, 20, Colors.white.withValues(alpha: 0.10))),
        ),
        Positioned(
          bottom: 20, left: -15,
          child: Transform.rotate(angle: -0.15, child: _rect(50, 15, Colors.white.withValues(alpha: 0.08))),
        ),
        Positioned(top: 50, left: 15, child: _icon(Icons.access_time, 12, 0.30)),
      ],
    );

Widget _stars({required int count}) => Stack(
      children: [
        Positioned(top: -20, right: -20, child: _circle(65, Colors.white.withValues(alpha: 0.07))),
        Positioned(bottom: -15, left: -15, child: _circle(45, Colors.white.withValues(alpha: 0.09))),
        Positioned(top: 12, left: 14, child: _icon(Icons.star, 8, 0.30)),
        Positioned(bottom: 30, right: 14, child: _icon(Icons.star, 5, 0.20)),
        if (count >= 3)
          Positioned(top: 40, right: 8, child: _icon(Icons.star, 6, 0.25)),
      ],
    );

Widget _rects(IconData icon) => Stack(
      children: [
        Positioned(
          top: -15, left: -15,
          child: Transform.rotate(angle: 0.3, child: _rect(50, 50, Colors.white.withValues(alpha: 0.1))),
        ),
        Positioned(
          bottom: -20, right: -10,
          child: Transform.rotate(angle: -0.5, child: _rect(40, 40, Colors.white.withValues(alpha: 0.08))),
        ),
        Positioned(top: 15, right: 15, child: _icon(icon, 14, 0.3)),
      ],
    );

Widget _bubbles(IconData icon) => Stack(
      children: [
        Positioned(top: -25, right: 20, child: _circle(50, Colors.white.withValues(alpha: 0.12))),
        Positioned(bottom: -15, left: 30, child: _circle(35, Colors.white.withValues(alpha: 0.10))),
        Positioned(top: 40, left: 5, child: _circle(15, Colors.white.withValues(alpha: 0.15))),
        Positioned(bottom: 30, right: 10, child: _icon(icon, 16, 0.25)),
      ],
    );

Widget _singleIcon(IconData icon, {double iconSize = 14}) => Stack(
      children: [
        Positioned(top: -20, right: -20, child: _circle(60, Colors.white.withValues(alpha: 0.10))),
        Positioned(bottom: -15, left: -15, child: _circle(50, Colors.white.withValues(alpha: 0.08))),
        Positioned(top: 15, right: 12, child: _icon(icon, iconSize, 0.3)),
      ],
    );

Widget _doubleIcon(IconData icon1, IconData icon2) => Stack(
      children: [
        Positioned(top: -20, left: -20, child: _circle(70, Colors.white.withValues(alpha: 0.08))),
        Positioned(bottom: -15, right: -15, child: _circle(55, Colors.white.withValues(alpha: 0.10))),
        Positioned(top: 15, right: 12, child: _icon(icon1, 14, 0.30)),
        Positioned(bottom: 35, left: 12, child: _icon(icon2, 10, 0.25)),
      ],
    );
