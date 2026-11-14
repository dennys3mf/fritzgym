# Fritz Gym deployment

Python 3.13 / Django / PostgreSQL / Heroku. `Procfile` runs migrations in the
release phase. WhiteNoise serves the versioned static files built by Heroku.
The public theme lives in `templates/fritz/` and retains the original logo.

To preview the curated catalog changes:

    python manage.py cargar_guias --dry-run

To install or refresh the 15 curated guides:

    python manage.py cargar_guias

This command matches names and aliases, preserves existing machine IDs and QR
links, keeps approved existing videos, and never deletes unrelated records.
It refreshes descriptions of the known guides; run it intentionally after
reviewing any editorial changes made in the admin. It is not run on every deploy.

Validation:

    python manage.py test maquinas
    python manage.py collectstatic --noinput

Video sources: Nova Southeastern University RecWell exercise library
(https://www.rec.nova.edu/recreational-complex/exercise-library.html),
Muscle & Strength's Smith squat guide
(https://www.muscleandstrength.com/exercises/smith-machine-squat.html), and the
existing publishers credited on their respective detail pages. New videos were
checked with YouTube's oEmbed endpoint on 2026-11-14. Availability and regional
embedding restrictions can change independently of the site.
