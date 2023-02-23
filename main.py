import pygame
from pygame import mixer

mixer.init()
mixer.music.load("src//Galaxy Collapse.mp3")
mixer.music.set_volume(0.2)

pygame.init()
fps = 180
bpm = 270
screen = pygame.display.set_mode((1280, 720))
RedNoteSprite = pygame.image.load("src//RedNote.png")
PinkNoteSprite = pygame.image.load("src//PinkNote.png")
BarSprite = pygame.image.load("src//bar.png")
firstLine = []
secondLine = []
thirdLine = []
fourthLine = []
notesList = [firstLine, secondLine, thirdLine, fourthLine]
FirstLineX = 340  # First Line X Coordinates
SecondLineX = 340 + 130  # Second Line X Coordinates
ThirdLineX = 340 + 260  # Third Line X Coordinates
FourthLineX = 340 + 390  # Fourth Line X Coordinates


class dUI:
    pass


class Conductor:
    def __init__(self) -> None:
        self.bpm = 270.0
        self.secPerBeat = self.bpm / 60


class Note:
    def __init__(self, x: float, y: float, line: int) -> None:
        self.x = x
        self.y = y
        self.isClickable = False
        self.line = line

    def DrawOnScreen(self, surface):
        # Drawing Red Notes for Line 1 and 4
        if self.line == 1 or self.line == 4:
            surface.blit(RedNoteSprite, (self.x, self.y))
        # Drawing Pink Notes for Line 2 and 3
        elif self.line == 2 or self.line == 3:
            surface.blit(PinkNoteSprite, (self.x, self.y))
        self.DropDown()
        self.UpdateStatus()

    def DropDown(self):
        self.y += 5.65

    def UpdateStatus(self):
        if self.y > 420 and self.y < 620:
            self.isClickable = True
        else:
            self.isClickable = False


class SingleNote(Note):
    def __init__(self, x: int, y: int, line: int) -> None:
        super().__init__(x, y, line)


class LongNote(Note):
    def __init__(self, x: int, y: int, line: int, distance: int) -> None:
        super().__init__(x, y, line)
        self.distance = distance


def spawn_note(line: int, timing: int) -> None:
    note = None
    if line == 1:
        note = SingleNote(FirstLineX, timing + 400 - 2 * timing, 1)
    elif line == 2:
        note = SingleNote(SecondLineX, timing + 400 - 2 * timing, 2)
    elif line == 3:
        note = SingleNote(ThirdLineX, timing + 400 - 2 * timing, 3)
    elif line == 4:
        note = SingleNote(FourthLineX, timing + 400 - 2 * timing, 4)
    notesList[line - 1].append(note)


def spawn_notes():
    level = open("src//res.rg")
    lines = level.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")
        lines[i] = [lines[i][0], lines[i][1].replace("\n", "")]
    print(lines)
    for i in reversed(lines):
        spawn_note(int(i[0]), int(i[1]))


def update_screen(pressedKeys, ExecuteOnce) -> None:
    # print(mixer.music.get_pos())
    screen.fill((20, 20, 20))
    screen.blit(BarSprite, (355, 600))
    for i in range(0, 4):
        for j in range(0, len(notesList[i])):
            if notesList[i][j] != None:
                notesList[i][j].DrawOnScreen(screen)
    if pressedKeys[0] == pygame.K_a:
        if ExecuteOnce[0] == True:
            for note in range(len(notesList[0]) - 1, -1, -1):
                if (
                    notesList[0][note] != None
                    and notesList[0][note].isClickable == True
                ):
                    notesList[0][note] = None
                    break
            for i in range(0, 4):
                for j in range(0, len(notesList[i])):
                    if notesList[i][j] != None:
                        notesList[i][j].DrawOnScreen(screen)
            ExecuteOnce[0] = False
    if pressedKeys[1] == pygame.K_s:
        if ExecuteOnce[1] == True:
            for note in range(len(notesList[1]) - 1, -1, -1):
                if (
                    notesList[1][note] != None
                    and notesList[1][note].isClickable == True
                ):
                    notesList[1][note] = None
                    break
            for i in range(0, 4):
                for j in range(0, len(notesList[i])):
                    if notesList[i][j] != None:
                        notesList[i][j].DrawOnScreen(screen)
            ExecuteOnce[1] = False
    if pressedKeys[2] == pygame.K_k:
        if ExecuteOnce[2] == True:
            for note in range(len(notesList[2]) - 1, -1, -1):
                if (
                    notesList[2][note] != None
                    and notesList[2][note].isClickable == True
                ):
                    notesList[2][note] = None
                    break
            for i in range(0, 4):
                for j in range(0, len(notesList[i])):
                    if notesList[i][j] != None:
                        notesList[i][j].DrawOnScreen(screen)
            ExecuteOnce[2] = False
    if pressedKeys[3] == pygame.K_l:
        if ExecuteOnce[3] == True:
            for note in range(len(notesList[3]) - 1, -1, -1):
                if (
                    notesList[3][note] != None
                    and notesList[3][note].isClickable == True
                ):
                    notesList[3][note] = None
                    break
            for i in range(0, 4):
                for j in range(0, len(notesList[i])):
                    if notesList[i][j] != None:
                        notesList[i][j].DrawOnScreen(screen)
            ExecuteOnce[3] = False
    pygame.display.update()
    return ExecuteOnce


def main():
    mixer.music.play()
    ExecuteOnce1stLine = True
    ExecuteOnce2ndLine = True
    ExecuteOnce3rdLine = True
    ExecuteOnce4thLine = True
    spawn_notes()
    clock = pygame.time.Clock()
    running = True
    ExecuteOnce = [
        ExecuteOnce1stLine,
        ExecuteOnce2ndLine,
        ExecuteOnce3rdLine,
        ExecuteOnce4thLine,
    ]
    while running:
        clock.tick(fps)
        pressedKeys = [None, None, None, None]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pressedKeys[0] = pygame.K_a
                if event.key == pygame.K_s:
                    pressedKeys[1] = pygame.K_s
                if event.key == pygame.K_k:
                    pressedKeys[2] = pygame.K_k
                if event.key == pygame.K_l:
                    pressedKeys[3] = pygame.K_l
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    pressedKeys[0] = None
                    ExecuteOnce[0] = True
                elif event.key == pygame.K_s:
                    pressedKeys[1] = None
                    ExecuteOnce[1] = True
                elif event.key == pygame.K_k:
                    pressedKeys[2] = None
                    ExecuteOnce[2] = True
                elif event.key == pygame.K_l:
                    pressedKeys[3] = None
                    ExecuteOnce[3] = True
        ExecuteOnce = update_screen(pressedKeys, ExecuteOnce)
    pygame.quit()


if __name__ == "__main__":
    main()
