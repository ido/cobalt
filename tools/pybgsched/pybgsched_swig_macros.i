
/*macro to make the boost.shared_ptr template construct
wraping cleaner.*/
%define PYBGSCHED_SHARED_PTR_VECTORS(class)

%template(class ## PtrVector) std::vector< bgsched:: ## class ## ::Ptr >;
%template(class ## CPtrVector) std::vector< bgsched:: ## class ## ::ConstPtr >;

%enddef

/*This is used in converting enums returns to strings.
  This gets used all over the place.
*/
%define PYBGSCHED_CASE_ENUM_TO_STRING(class, name)
    case class ## :: ## name ## :
        return std::string( #name );
        break;
%enddef
