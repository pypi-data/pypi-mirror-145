from kabaret import flow
from kabaret.flow_entities.entities import Entity, Property

from libreflow.utils.kabaret.flow_entities.entities import EntityView
from libreflow.baseflow.maputils import SimpleCreateAction
from libreflow.baseflow.file import CreateDefaultFilesAction
from libreflow.baseflow.departments import Department
from libreflow.baseflow.users import ToggleBookmarkAction

from .file import FileSystemMap
from .packaging import PackAction, CreateLayoutPackagesAction, CreateCleanPackagesAction


class CreateDepartmentDefaultFilesAction(CreateDefaultFilesAction):

    _department = flow.Parent()

    def get_target_groups(self):
        return [self._department.name()]

    def get_file_map(self):
        return self._department.files


class Department(flow.Object):

    _short_name = flow.Param()

    toggle_bookmark = flow.Child(ToggleBookmarkAction)

    files = flow.Child(FileSystemMap).ui(
        expanded=True,
        action_submenus=True,
        items_action_submenus=True
    )

    create_default_files = flow.Child(CreateDepartmentDefaultFilesAction)

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]} · {split[7]} · {split[9]}'
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                department=self.name(),
                department_short_name=self._short_name.get() if self._short_name.get() is not None else self.name(),
            )


class CleanDepartment(Department):

    _short_name = flow.Param('cln')


class CompDepartment(Department):

    _short_name = flow.Param('comp')


class MiscDepartment(Department):

    pack = flow.Child(PackAction).ui(label='Create package')

    _short_name = flow.Param('misc')
    _label = flow.Param()

    def _fill_ui(self, ui):
        label = self._label.get()
        if label:
            ui['label'] = label


class ShotDepartments(flow.Object):

    misc        = flow.Child(MiscDepartment)
    clean       = flow.Child(CleanDepartment).ui(label='Clean-up')
    compositing = flow.Child(CompDepartment)


class Shot(Entity):

    ICON = ('icons.flow', 'shot')

    shotgrid_id = Property().ui(label='ShotGrid ID', hidden=True)

    departments = flow.Child(ShotDepartments).ui(expanded=True)

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]} · {split[7]}'

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(shot=self.name())


class CreateSGShots(flow.Action):

    ICON = ('icons.flow', 'shotgrid')

    skip_existing = flow.SessionParam(False).ui(editor='bool')

    _shots = flow.Parent()
    _sequence = flow.Parent(2)

    def get_buttons(self):
        return ['Create shots', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        skip_existing = self.skip_existing.get()
        shots_data = self.root().project().get_shotgrid_config().get_shots_data(
            self._sequence.shotgrid_id.get()
        )
        for data in shots_data:
            name = data['name'].lower()

            if not self._shots.has_mapped_name(name):
                s = self._shots.add(name)
            elif not skip_existing:
                s = self._shots[name]
            else:
                continue
            
            print(f'Create shot {self._sequence.name()} {data["name"]}')
            s.shotgrid_id.set(data['shotgrid_id'])
        
        self._shots.touch()


class Shots(EntityView):

    ICON = ('icons.flow', 'shot')

    create_shot = flow.Child(SimpleCreateAction)
    create_shots = flow.Child(CreateSGShots)
    
    @classmethod
    def mapped_type(cls):
        return Shot
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.shots.collection_name()
    
    def columns(self):
        return ['Name']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.name()


class Sequence(Entity):

    ICON = ('icons.flow', 'sequence')

    shotgrid_id = Property().ui(label='ShotGrid ID', hidden=True)
    shots = flow.Child(Shots).ui(
        expanded=True, 
        show_filter=True
    )

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]}'

    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(sequence=self.name())


class CreateSGSequences(flow.Action):

    ICON = ('icons.flow', 'shotgrid')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    create_shots = flow.SessionParam(False).ui(editor='bool')

    _sequences = flow.Parent()

    def get_buttons(self):
        return ['Create sequences', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        sequences_data = self.root().project().get_shotgrid_config().get_sequences_data()
        create_shots = self.create_shots.get()
        skip_existing = self.skip_existing.get()

        for data in sequences_data:
            name = data['name'].lower()

            if not self._sequences.has_mapped_name(name):
                s = self._sequences.add(name)
            elif not skip_existing:
                s = self._sequences[name]
            else:
                continue
            
            print(f'Create sequence {data["name"]}')
            s.shotgrid_id.set(data['shotgrid_id'])

            if create_shots:
                s.shots.create_shots.skip_existing.set(skip_existing)
                s.shots.create_shots.run('Create shots')
        
        self._sequences.touch()


class Sequences(EntityView):

    ICON = ('icons.flow', 'sequence')

    create_sequence = flow.Child(SimpleCreateAction)
    create_sequences = flow.Child(CreateSGSequences)
    
    @classmethod
    def mapped_type(cls):
        return Sequence
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.sequences.collection_name()
    
    def columns(self):
        return ['Name']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.name()


class PackageTypeChoiceValue(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'
    CHOICES = ['Layout', 'Clean']

    _action = flow.Parent()

    def choices(self):
        return self.CHOICES
    
    def revert_to_default(self):
        values = self.root().project().get_action_value_store().get_action_values(
            self._action.name(), {self.name(): self.get()}
        )
        value = values[self.name()]

        if value in self.choices():
            self.set(value)


class CreatePackagesAction(flow.Action):

    ICON = ('icons.gui', 'package')

    package_type = flow.SessionParam('Layout', PackageTypeChoiceValue)

    _film = flow.Parent()

    def get_buttons(self):
        self.package_type.revert_to_default()
        return ['Select', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        if self.package_type.get() == 'Layout':
            ret = self.get_result(
                next_action=self._film.create_layout_packages.oid()
            )
        else:
            ret = self.get_result(
                next_action=self._film.create_clean_packages.oid()
            )
        
        return ret


class Film(Entity):

    ICON = ('icons.flow', 'film')

    sequences = flow.Child(Sequences).ui(
        expanded=True,
        show_filter=True
    )
    create_packages        = flow.Child(CreatePackagesAction)
    create_layout_packages = flow.Child(CreateLayoutPackagesAction).ui(hidden=True)
    create_clean_packages  = flow.Child(CreateCleanPackagesAction).ui(hidden=True)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(film=self.name())


class Films(EntityView):

    ICON = ('icons.flow', 'film')

    create_film = flow.Child(SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Film
    
    def collection_name(self):
        return self.root().project().get_entity_manager().films.collection_name()
