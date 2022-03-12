-- WORDS, a Latin dictionary, by Colonel William Whitaker (USAF, Retired)
--
-- Copyright William A. Whitaker (1936–2010)
--
-- This is a free program, which means it is proper to copy it and pass
-- it on to your friends. Consider it a developmental item for which
-- there is no charge. However, just for form, it is Copyrighted
-- (c). Permission is hereby freely given for any and all use of program
-- and data. You can sell it as your own, but at least tell me.
--
-- This version is distributed without obligation, but the developer
-- would appreciate comments and suggestions.
--
-- All parts of the WORDS system, source code and data files, are made freely
-- available to anyone who wishes to use them, for whatever purpose.

with Ada.Text_IO;
package Support_Utils.Word_Parameters is
   --  This package defines a number of parameters that are used in the program
   --  The default values are set in the body, so that they may be changed
   --  easily

   Change_Parameters_Character        : Character := '#';
   Change_Language_Character          : Character := '~';
   Help_Character                     : Character := '?';

   --  These files are used by the program if requested, but not necessary
   --  They are all text files and human readable

   --  MODE_FILE is used by the program to remember MODE values between runs
   Mode_File : Ada.Text_IO.File_Type;

   --  OUTPUT is used to Write out and save the results of a run
   Output : aliased Ada.Text_IO.File_Type;
   Input  : Ada.Text_IO.File_Type;
   --  UNKNOWNS is used to record the words that the program fails to find
   Unknowns : Ada.Text_IO.File_Type;

   --  This is a flag to tell if there has been Trim ming for this word
   -- FIXME : this obviously should not exist
   Trimmed : Boolean := False;

   type Mode_Type is (
     Trim_Output,
     Have_Output_File,
     Write_Output_To_File,
     Do_Unknowns_Only,
     Write_Unknowns_To_File,
     Ignore_Unknown_Names,
     Ignore_Unknown_Caps,
     Do_Compounds,
     Do_Fixes,
     Do_Tricks,
     Do_Dictionary_Forms,
     Show_Age,
     Show_Frequency,
     Do_Examples,
     Do_Only_Meanings,
     Do_Stems_For_Unknown
                     );

   package Mode_Type_Io is new Ada.Text_IO.Enumeration_IO (Mode_Type);

   type Mode_Array is array (Mode_Type) of Boolean;

   Words_Mode : Mode_Array;        --  Initialized in body

   procedure Change_Parameters;

   procedure Initialize_Word_Parameters;

end Support_Utils.Word_Parameters;
