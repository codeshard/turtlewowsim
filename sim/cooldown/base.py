from sim.character import Character


class Cooldown:
    STARTS_CD_ON_ACTIVATION = True
    PRINTS_ACTIVATION = True
    TRACK_UPTIME = False

    def __init__(self, character: Character):
        self.character = character
        self._on_cooldown = False
        self._active = False

    @property
    def duration(self):
        return 0

    @property
    def cooldown(self):
        return 0

    @property
    def env(self):
        return self.character.env

    @property
    def usable(self):
        return not self._active and not self._on_cooldown

    @property
    def on_cooldown(self):
        return self._on_cooldown

    def is_active(self):
        return self._active

    @property
    def name(self):
        return type(self).__name__

    def track_buff_start_time(self):
        if self.name not in self.character.buff_start_times:
            self.character.buff_start_times[self.name] = self.character.env.now

    def track_buff_uptime(self):
        if self.name not in self.character.buff_uptimes:
            self.character.buff_uptimes[self.name] = 0
        self.character.buff_uptimes[self.name] += (
            self.character.env.now - self.character.buff_start_times[self.name]
        )

        del self.character.buff_start_times[self.name]

    def activate(self):
        if self.usable:
            self._active = True

            if self.TRACK_UPTIME:
                self.track_buff_start_time()

            if self.PRINTS_ACTIVATION:
                self.character.print(f"{self.name} activated")

            cooldown = self.cooldown
            if self.STARTS_CD_ON_ACTIVATION and cooldown:
                self._on_cooldown = True

                def callback(self, cooldown):
                    yield self.env.timeout(cooldown)
                    if self.PRINTS_ACTIVATION:
                        self.character.print(
                            f"{self.name} cooldown ended after {cooldown} seconds"  # noqa E501
                        )

                    self._on_cooldown = False

                self.character.env.process(callback(self, cooldown))

            if self.duration:

                def callback(self):
                    yield self.character.env.timeout(self.duration)
                    self.deactivate()

                self.character.env.process(callback(self))
            else:
                self.deactivate()

    def deactivate(self):
        if self._active and self.TRACK_UPTIME:
            # add to uptime
            self.track_buff_uptime()

        self._active = False

        if self.PRINTS_ACTIVATION:
            self.character.print(f"{self.name} deactivated")

        cooldown = self.cooldown
        if not self.STARTS_CD_ON_ACTIVATION and cooldown:
            self._on_cooldown = True

            def callback(self, cooldown):
                yield self.env.timeout(cooldown)
                if self.PRINTS_ACTIVATION:
                    self.character.print(
                        f"{self.name} cooldown ended after {cooldown} seconds"
                    )

                self._on_cooldown = False

            self.character.env.process(callback(self, cooldown))
